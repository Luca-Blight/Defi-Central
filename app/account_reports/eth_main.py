import json
import os
import requests
import pytz
import time
import logging
import asyncio
import pandas as pd

from web3 import Web3
from itertools import chain
from datetime import datetime
from helper import get_block_date, get_transaction_fee
from account_info import contract_table, wallet_table
from models.AccountLedger import AccountLedger
from models.Account import Account
from database.main import async_engine
from accounts import eth_account_addresses

from app.core.config import Settings
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
from sqlmodel import insert, and_

from dotenv import load_dotenv

load_dotenv()

settings = Settings()


@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    session = async_session()

    try:
        yield session
    finally:
        await session.close()


# make async


logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname} {message}",
    style="{",
    datefmt="%m-%d-%y %H:%M:%S",
)

log = logging.getLogger()


contract_names = list(contract_table.values())
contract_addresses = list(contract_table.keys())

wallet_names = list(account_table.values())
wallet_addresses = list(account_table.keys())


# if wallet not in contract names, then it is a user wallet
async def map_stream(
    stream: list, wallet_id: str, wallet_account: str, currency_type: str
) -> list[dict]:
    attributes = [
        "wallet_id",
        "from_wallet",
        "to_wallet",
        "block_number",
        "currency",
        "transaction_hash",
        "quantity",
        "block_date",
        "created_at",
    ]

    zero_address = "0x0000000000000000000000000000000000000000"

    records = []

    texas_timezone = pytz.timezone("US/Central")
    created_at = pd.Timestamp(datetime.now(tz=texas_timezone))
    skipped = 0

    for rawResult in stream:
        if rawResult.status_code == 400:
            log.error("stream error, status code 400")
        else:
            result = json.loads(rawResult.text)
            if result and result.get("result", None):
                log.info(
                    f"This is the response received from {wallet_id} of {wallet_account}: {result}"
                )
                if result["result"].get("transfers", None):
                    result: list[dict] = result["result"]["transfers"]
                    for data in result:
                        if (
                            data["asset"] == "ETH"
                            or data["asset"] == "MATIC"
                            or data["asset"] == "ART"
                            or data["category"] == "erc721"
                            or data["asset"] == None
                        ):
                            currency: str = currency_type.value

                            block_number: int = Web3.toInt(hexstr=str(data["blockNum"]))
                            block_date: pd.Timestamp = get_block_date(
                                block_number, currency
                            )
                            transaction_hash: str = data["hash"]
                            from_wallet: str = (
                                data["from"]
                                if data["from"] != zero_address
                                else wallet_account
                            )
                            to_wallet: str = data["to"]
                            if (wallet_id in contract_names) and (
                                wallet_table.get(from_wallet, None)
                            ):  # if the wallet/account is a contract and the from_wallet is a wallet of ours, then skip. This avoids double counting.
                                log.info(
                                    f"""skipping contract event under {wallet_id} for transaction_hash: {transaction_hash} from_wallet: {from_wallet} to_wallet: {to_wallet} block_date:{block_date}, because it is already under events for ["""
                                )
                                skipped += 1
                                continue
                            else:
                                data["value"] = (
                                    0 if data["value"] == None else data["value"]
                                )
                                quantity: float = (
                                    data["value"]
                                    if data["value"] > 0
                                    else get_transaction_fee(transaction_hash, currency)
                                )
                                records.append(
                                    dict(
                                        zip(
                                            attributes,
                                            [
                                                wallet_id,
                                                from_wallet,
                                                to_wallet,
                                                block_number,
                                                currency,
                                                transaction_hash,
                                                quantity,
                                                block_date,
                                                created_at,
                                            ],
                                        )
                                    )
                                )
                        else:
                            pass

    length_of_records: int = len(records)

    log.info(records) if records else None

    log.info(
        f"There are {length_of_records} transactions in this query associated with {wallet_id} of {wallet_account} and {skipped} were skipped to avoid double counting."
    )
    return records


async def extract_stream(account: object, idx: int) -> pd.DataFrame:
    eth_walletledger_records = []
    eth_wallet_records = []

    account_id, account_address, account_currency, account_block_number = (
        account.account_id,
        account.account,
        account.currency,
        account.block_number,
    )

    ALCHEMY_URL: str = (
        "POLYGON_ALCHEMY_URL"
        if account_currency.value == "MATIC"
        else "ETH_ALCHEMY_URL"
    )

    hex_block_number: str = (
        Web3.toHex(account_block_number) if account_block_number else "latest"
    )

    try:
        log.info(
            f"attempting request(from) with account {account_address} of {account_id}, starting from block_number: {account_block_number}"
        )

        stream_from = requests.post(
            url=os.environ.get(ALCHEMY_URL),
            json={
                "jsonrpc": "2.0",
                "id": 0,
                "method": "alchemy_getAssetTransfers",
                "params": [
                    {
                        "fromBlock": f"{hex_block_number}",
                        "toBlock": "latest",
                        "fromAddress": f"{account_address}",
                        "excludeZeroValue": False,
                        "category": [
                            "external",
                            "internal",
                            "erc721",
                            "erc20",
                            "erc1155",
                        ],
                    }
                ],
            },
        )
        log.info(
            f"attempting request(to) with wallet account {account_address} of {account_id}, starting from block_number:{account_block_number}"
        )

        stream_to = requests.post(
            url=os.environ.get(ALCHEMY_URL),
            json={
                "jsonrpc": "2.0",
                "id": 0,
                "method": "alchemy_getAssetTransfers",
                "params": [
                    {
                        "fromBlock": f"{hex_block_number}",
                        "toBlock": "latest",
                        "toAddress": f"{account_address}",
                        "excludeZeroValue": False,
                        "category": [
                            "external",
                            "internal",
                            "erc721",
                            "erc20",
                            "erc1155",
                        ],
                    }
                ],
            },
        )

        stream = [stream_from, stream_to]
    except Exception as e:
        log.error(
            f"request failed with wallet account {account_address} of {account_id}, starting from block_number:{account_block_number}, error: {e}"
        )

    mapped_data: list[dict] = map_stream(
        stream, account_id, account_address, account_currency
    )

    if mapped_data:
        eth_walletledger_records.append(mapped_data)
    else:
        pass

    if mapped_data:
        mapped_data: list[dict] = sorted(mapped_data, key=lambda x: x["block_date"])

        # logging.info(f"mapped_data: {mapped_data}")

        eth_wallet_records.append(
            {
                "wallet_id": account_id,
                "account": account_address,
                "block_number": mapped_data[-1]["block_number"],
                "block_date": mapped_data[-1]["block_date"],
                "transaction_hash": mapped_data[-1]["transaction_hash"],
                "currency": mapped_data[-1]["currency"],
                "created_at": mapped_data[-1]["created_at"],
            }
        )
    else:
        pass

    if len(eth_walletledger_records) > 1:
        # flattens out collection of list of records(each wallet report)
        wl_df = pd.DataFrame(list(chain.from_iterable(eth_walletledger_records)))

        w_df = pd.DataFrame(eth_walletledger_records)

        return wl_df, w_df
    else:
        wl_df = pd.DataFrame(mapped_data)

        w_df = pd.DataFrame(eth_wallet_records)

        return wl_df, w_df


async def load_eth_stream(
    account: str, wl_transactions: pd.DataFrame, w_transactions: pd.DataFrame
) -> pd.DataFrame:
    if wl_transactions.empty:
        log.info(
            f"Because there are 0 transactions with {account.wallet_id}, this load has been stopped"
        )
    else:
        # drop duplicates to prevent redundant transactions from being recorded, where multiple mints are concerned
        account_ledger_records: list[dict] = (
            wl_transactions[
                [
                    "wallet_id",
                    "to_wallet",
                    "from_wallet",
                    "transaction_hash",
                    "block_number",
                    "block_date",
                    "quantity",
                    "currency",
                    "created_at",
                ]
            ]
            .drop_duplicates(subset=["transaction_hash", "quantity"], keep="first")
            .to_dict("records")
        )

        async with get_async_session() as session:
            insert_stmt = insert(AccountLedger).values(account_ledger_records)

            results = session.execute(insert_stmt).rowcount
            session.commit()

            log.info(
                f"{account.wallet_id} of account {account.account} has been loaded to to the wallet_ledger table, there were {results} changes"
            )

        wallet_record: pd.DataFrame = w_transactions[
            [
                "wallet_id",
                "account",
                "currency",
                "block_number",
                "transaction_hash",
                "block_date",
                "created_at",
            ]
        ].to_dict("records")[0]

        async with get_async_session() as session:
            account: str = wallet_record["account"]
            account = (
                session.query(Account)
                .filter(
                    and_(
                        Account.account_id == account.account_id,
                        Account.account == account,
                    )
                )
                .first()
            )
            account.transaction_hash = wallet_record["transaction_hash"]
            account.block_number = wallet_record["block_number"]
            account.block_date = wallet_record["block_date"]
            account.created_at = wallet_record["created_at"]

            session.commit()

            logging.info(
                f" wallet: {account.wallet_id} of {account}  has been updated with the most recent record for future extraction: {account.account_id} of {account} "
            )


def run_eth_pipeline(account_addresses: list[dict]):
    for idx, account in enumerate(account_addresses):
        time.sleep(3)

        log.info(f"running wallet {account} of account {account.account}, index {idx}")

        wl_stream: pd.DataFrame
        w_stream: pd.DataFrame

        wl_stream, w_stream = extract_stream(account, idx)
        load_eth_stream(account, wl_stream, w_stream)


if __name__ == "__main__":
    log.info("eth pipeline started")
    start = time.time()

    log.info(
        f"These are all the wallet addresses being run through the eth pipeline: {eth_account_addresses}"
    )

    asyncio.run(run_eth_pipeline(eth_account_addresses))

    log.info(f"cleaning wallet_ledger table of duplicates")
    # cleans edge case duplicates in wallet_ledger table

    end = time.time()
    log.info(f"eth pipeline finished, total time elapsed: {end - start} seconds")

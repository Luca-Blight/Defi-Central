import http.client
import json
import ssl
import os
import grpc
import time
import pytz
import pandas as pd

from app.graphql.graphql_pb2_grpc import *
from app.graphql.graphql_pb2 import Request
from google.protobuf.struct_pb2 import Struct
from app.account_reports.query import Query
from itertools import chain
from datetime import datetime

from app.account_reports.accounts import Account

from app.models.Account import Account
from app.models.AccountLedger import AccountLedger
from sqlalchemy.dialects.postgresql import insert as Insert
from sqlalchemy import Integer, and_
from app.models.ConversionRate import *
from typing import List, Optional
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from database.main import async_engine
from contextlib import asynccontextmanager


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


ssl._create_default_https_context = ssl._create_unverified_context


def token_for_api_key(api_key: str) -> str:
    connection = http.client.HTTPSConnection("auth.eosnation.io")
    connection.request(
        "POST",
        "/v1/auth/issue",
        json.dumps({"api_key": api_key}),
        {"Content-type": "application/json"},
    )
    response = connection.getresponse()

    if response.status != 200:
        raise Exception(f" Status: {response.status} reason: {response.reason}")

    token = json.loads(response.read().decode())["token"]
    connection.close()
    return token


def create_client(endpoint: str) -> object:
    api_key = os.environ.get("DFUSE_API_KEY")
    if api_key == None:
        raise Exception("you must specify a DFUSE_API_KEY environment variable")

    token = token_for_api_key(api_key)
    credentials = grpc.access_token_call_credentials(token)

    channel = grpc.secure_channel(
        endpoint,
        credentials=grpc.composite_channel_credentials(
            grpc.ssl_channel_credentials(), credentials
        ),
    )
    return GraphQLStub(channel)


def map_stream(
    stream: object, account_id: str, account: str, currency_type: str, idx: int
) -> List[dict]:
    attributes = [
        "cursor",
        "account",
        "block_date",
        "block_number",
        "currency",
        "transaction_hash",
        "global_sequence",
        "action",
        "wallet_id",
        "from_wallet",
        "to_wallet",
        "quantity",
        "memo",
        "counter",
        "created_at",
    ]

    records = []

    texas_timezone = pytz.timezone("US/Central")
    created_at = pd.Timestamp(datetime.now(tz=texas_timezone))

    for rawResult in stream:
        if rawResult.errors:
            print("An error occurred")
            print(rawResult.errors)
        else:
            result = json.loads(rawResult.data)

            for data in result["searchTransactionsForward"]["trace"]["matchingActions"]:
                undo = result["searchTransactionsForward"]["undo"]
                quantity, currency = data["json"]["quantity"].split(" ")
                if (undo == False) and (currency_type == currency):
                    cursor = result["searchTransactionsForward"]["cursor"]
                    quantity = float(quantity)
                    block_date = pd.Timestamp(
                        result["searchTransactionsForward"]["trace"]["block"][
                            "timestamp"
                        ]
                    )
                    block_number = result["searchTransactionsForward"]["trace"][
                        "block"
                    ]["num"]
                    transaction_hash = result["searchTransactionsForward"]["trace"][
                        "id"
                    ]
                    action = data["name"]
                    account = account
                    counter = idx
                    from_wallet = data["json"]["from"]
                    to_wallet = data["json"]["to"]
                    memo = data["json"]["memo"]
                    global_sequence = data["seq"]
                    records.append(
                        dict(
                            zip(
                                attributes,
                                [
                                    cursor,
                                    account,
                                    block_date,
                                    block_number,
                                    currency,
                                    transaction_hash,
                                    global_sequence,
                                    action,
                                    account_id,
                                    from_wallet,
                                    to_wallet,
                                    quantity,
                                    memo,
                                    counter,
                                    created_at,
                                ],
                            )
                        )
                    )

    length_of_records = len(records)
    print(
        f"There are {length_of_records} transactions in this query associated with {account_id} and account {account}"
    )
    return records


def extract_stream(wallet: object, idx: int) -> pd.DataFrame:
    client = create_client(os.environ.get("WAX_URL"))

    walletledger_records = []
    wallet_records = []

    wallet_id = wallet.wallet_id
    wallet_account = wallet.account
    wallet_cursor = wallet.cursor
    block_number = wallet.block_number
    currency_type = wallet.currency.value
    variables = Struct()

    # must use struct variable for graphql query.
    variables[
        "query"
    ] = f"account:{wallet_account} receiver:{wallet_account} action:transfer (data.from:{wallet_id} OR data.to:{wallet_id})"
    variables["cursor"] = wallet_cursor
    variables["low"] = block_number
    variables["high"] = -1
    variables["limit"] = 50000

    print(f"running wallet {wallet_id} of account {wallet_account}, index {idx}")

    try:
        stream = client.Execute(Request(query=Query, variables=variables))
    finally:
        mapped_data = map_stream(stream, wallet_id, wallet_account, currency_type, idx)

        if mapped_data:
            walletledger_records.append(mapped_data)
        else:
            pass

        if mapped_data:
            # sorts by block_date, we want the last(most recent) record for the wallet table
            mapped_data = sorted(mapped_data, key=lambda x: x["block_date"])

            wallet_records.append(
                {
                    "wallet_id": wallet_id,
                    "block_number": block_number,
                    "block_date": mapped_data[-1]["block_date"],
                    "transaction_hash": mapped_data[-1]["transaction_hash"],
                    "account": mapped_data[-1]["account"],
                    "cursor": mapped_data[-1]["cursor"],
                    "currency": mapped_data[-1]["currency"],
                    "counter": mapped_data[-1]["counter"],
                    "created_at": mapped_data[-1]["created_at"],
                }
            )
        else:
            pass

        if len(walletledger_records) > 1:
            wl_df = pd.DataFrame(list(chain.from_iterable(walletledger_records)))
            w_df = pd.DataFrame(wallet_records)
            return wl_df, w_df
        else:
            wl_df = pd.DataFrame(mapped_data)
            w_df = pd.DataFrame(wallet_records)
            return wl_df, w_df


async def load_stream(
    wl_transactions: Optional[pd.DataFrame],
    w_transactions: Optional[pd.DataFrame],
    wallet: str,
    current_counter: int,
) -> pd.DataFrame:
    if wl_transactions.empty:
        async with get_async_session() as session:
            session.query(Account).update({Account.counter: current_counter})
            print(
                f"counter for all wallets has been updated with {current_counter}, no records from this wallet:{wallet.wallet_id} of account {wallet.account}"
            )
    else:
        wallet_record = w_transactions[
            [
                "wallet_id",
                "currency",
                "account",
                "block_date",
                "cursor",
                "counter",
                "transaction_hash",
                "block_number",
                "created_at",
            ]
        ].to_dict("records")[
            0
        ]  # check for order of blocknumbers for query, because this is going off the last
        wallet_ledger_records = wl_transactions[
            [
                "wallet_id",
                "to_wallet",
                "from_wallet",
                "transaction_hash",
                "global_sequence",
                "block_date",
                "block_number",
                "action",
                "quantity",
                "currency",
                "cursor",
                "memo",
                "created_at",
            ]
        ].to_dict(
            "records"
        )  # add account

        async with get_async_session() as session:
            account = wallet_record["account"]

            wallet_result = (
                session.query(Account)
                .filter(
                    and_(
                        Account.wallet_id == wallet.wallet_id,
                        Account.account == account,
                    )
                )
                .first()
            )

            wallet_result.cursor = wallet_record["cursor"]
            wallet_result.transaction_hash = wallet_record["transaction_hash"]
            wallet_result.block_date = wallet_record["block_date"]
            wallet_result.counter = wallet_record["counter"]
            wallet_result.created_at = wallet_record["created_at"]

            session.commit()
            print(
                f"{wallet_result.wallet_id} of account {wallet_result.account} has been updated in the wallet table."
            )

        async with get_async_session() as session:
            account = wallet_record["account"]

            insert_stmt = Insert(AccountLedger).values(wallet_ledger_records)
            do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
                index_elements=["global_sequence"]
            )
            results = session.execute(do_nothing_stmt).rowcount

            print(
                f"{wallet.wallet_id} of account {account} has been loaded to to the wallet_ledger table, there were {results} changes"
            )

        async with get_async_session() as session:
            session.query(Account).update({Account.counter: wallet_record["counter"]})

            session.commit()
            print(
                f"counter updated to {wallet_record['counter']}, associated with {wallet_record['account']}"
            )


def initiate(wallets: List[WalletAddress], starting_counter: int) -> str:
    for idx, wallet in enumerate(wallets[starting_counter:]):
        time.sleep(5)
        current_counter = starting_counter + idx

        wl_stream, w_stream = extract_stream(wallet, idx=current_counter)
        load_stream(wl_stream, w_stream, wallet, current_counter)

        if (len(wallets) - 1) == current_counter:
            async with get_async_session() as session:
                session.query(Account).update({Account.counter: 0})
                session.commit()

            return print(
                f"all available wallet transactions have been loaded and counter reset to 0,{wallet.wallet_id} of {wallet.account} was the last wallet to run"
            )
        else:
            continue


def run_dfuse_pipeline(wallets: list[Account]):
    """

    This pipeline will extract,map/transform, and load each wallet.
    The extraction method used is gRPC over graphql, which is recommended by dfuse and is highly performant.
    All records will be loaded through sqlalchemy and will have a counter value associated with the load, so the pipeline can always pick back up where it left off.

    """

    initial_table = pd.read_sql("SELECT * FROM wallet LIMIT 1;", async_engine)

    if initial_table.empty:
        # condition triggered on the first pull, subsequent pulls will trigger the else statement
        starting_counter = 0

        initiate(wallets, starting_counter)

    else:
        starting_counter = int(initial_table["counter"][0])

        initiate(wallets, starting_counter)


def update_wallet_report_view():
    walletledger_table = pd.read_sql(
        "SELECT DISTINCT wallet_id,to_wallet,from_wallet,memo,CAST(quantity as float),currency,transaction_hash,block_date,block_number FROM wallet_ledger;",
        async_engine,
    )

    if walletledger_table.empty:
        print("view function ran but walletledger table is empty")
        pass
    else:
        walletledger_table = walletledger_table[
            ~(
                (walletledger_table["currency"] == "ETH")
                & (walletledger_table["transaction_hash"].duplicated())
            )
        ]
        walletledger_table["block_date"] = walletledger_table["block_date"].dt.round(
            "min"
        )
        conversion_rate_table = pd.read_sql(
            "SELECT DISTINCT block_date,CAST(waxp_conversion_rate as float),CAST(eth_conversion_rate as float),CAST(matic_conversion_rate as float) FROM conversion_rate;",
            async_engine,
        )
        walletledger_view = pd.merge(
            walletledger_table, conversion_rate_table, on=["block_date"], how="left"
        )
        walletledger_view.to_sql(
            con=async_engine,
            name="wallet_ledger_view",
            if_exists="replace",
            index_label="id",
            dtype={"id": Integer()},
        )
        print("view table for walletledger has been updated")


if __name__ == "__main__":
    run_dfuse_pipeline(dfuse_wallet_addresses)

    update_wallet_report_view()

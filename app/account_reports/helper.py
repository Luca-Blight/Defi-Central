import pandas as pd
import os

from web3 import Web3
from web3.middleware import geth_poa_middleware


matic_web3 = Web3(Web3.HTTPProvider(os.environ.get("POLYGON_ALCHEMY_URL")))
matic_web3.middleware_onion.inject(geth_poa_middleware, layer=0)
eth_web3 = Web3(Web3.HTTPProvider(os.environ.get("ETH_ALCHEMY_URL")))


async def get_block_date(block_number: int, currency: str) -> pd.Timestamp:
    web3: str = matic_web3 if currency == "MATIC" else eth_web3
    int_timestamp: int = await web3.eth.get_block(block_number)["timestamp"]
    block_date = pd.Timestamp(ts_input=int_timestamp, unit="s")
    return block_date


async def get_transaction_fee(transaction_hash: str, currency: str) -> float:
    web3: Web3 = matic_web3 if currency == "MATIC" else eth_web3

    gas_price: int = await web3.eth.getTransaction(transaction_hash).gasPrice
    gas_used: int = await web3.eth.getTransactionReceipt(transaction_hash).gasUsed
    transaction_fee: float = float(web3.fromWei(gas_price * gas_used, "ether"))

    return transaction_fee

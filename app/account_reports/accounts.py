from pydantic.dataclasses import dataclass
from database.main import async_engine
import pandas as pd
import enum


class CurrencyType(enum.Enum):

    """Definition of Protocol Type"""

    ETH = "ETH"
    MATIC = "MATIC"


@dataclass
class Account:
    id: int = None
    wallet_id: str = None
    currency: CurrencyType
    cursor: str = None
    block_number: int = None
    account: str = None

    """
    Extracts fixed wallet records corresponding to each wallet id from the wallet 
    table which allows the main.py file to pull entire list and run the pipeline.
    
    """


currency_enums = {"ETH": CurrencyType.ETH, "MATIC": CurrencyType.MATIC}

eth_accounts = pd.read_sql(
    """SELECT id, wallet_id, currency, cursor, block_number, account FROM wallet where currency = 'MATIC' or currency = 'ETH' ORDER BY id ASC """,
    async_engine,
).to_dict("records")

for account in eth_accounts:
    currency: str = account["currency"]
    account["currency"] = currency_enums[currency]

eth_account_addresses: list[Account] = [Account(**account) for account in eth_accounts]

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, DateTime, Float


class AccountLedger(SQLModel, table=True):
    __tablename__ = "account_ledger"

    id: int = Field(default=None, primary_key=True)
    account_id: str
    to_account: str
    quantity: float
    currency: str
    from_account: str
    cursor: str
    memo: str
    transaction_hash: str
    block_date: datetime
    block_number: int
    created_at: datetime = Field(default=datetime.utcnow)

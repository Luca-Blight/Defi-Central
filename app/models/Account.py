from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, DateTime


class Account(SQLModel, table=True):
    __tablename__ = "account"

    id: int = Field(default=None, primary_key=True)
    account_id: str
    cursor: str
    account_address: str
    block_date: datetime
    block_number: int
    transaction_hash: str
    currency: str
    counter: int
    description: Optional[str]
    contract: bool
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

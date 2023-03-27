from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column
import enum


class CurrencyType(enum.Enum):
    """Definition of Brand types"""

    ETH = "ETH"
    WETH = "MATIC"


class Collection(SQLModel, table=True):
    __tablename__ = "collection"

    id: int = Field(default=None, primary_key=True)
    name: Optional[str]
    chain: Optional[CurrencyType]

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, Float


class ConversionRate(SQLModel, table=True):
    __tablename__ = "conversion_rate"

    block_date: datetime = Field(primary_key=True)
    eth_conversion_rate: float
    matic_conversion_rate: float
    created_at: datetime = Field(default=datetime.utcnow)

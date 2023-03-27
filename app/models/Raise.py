from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, DateTime, Float


class Raise(SQLModel, table=True):
    __tablename__ = "raise"

    id: int = Field(default=None, primary_key=True)
    name: str
    round: int
    amount: float
    category: Optional[str]
    source: Optional[str]
    sector: Optional[str]
    source: Optional[str]
    investor_id: int = Field(default=None, foreign_key="investor.id")
    created_at = Column(DateTime, nullable=False)

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, DateTime


class Investor(SQLModel, table=True):
    __tablename__ = "investor"

    id: int = Field(default=None, primary_key=True)
    name: str
    fund: float
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

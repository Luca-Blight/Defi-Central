from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Financial(SQLModel, table=True):
    __tablename__ = "financial"

    id: int = Field(default=None, primary_key=True)
    tvl: Optional[float]
    fees: Optional[float]
    date: Optional[datetime]
    protocol_id: int = Field(foreign_key="protocol.id")
    created_at: datetime = Field(default=datetime.utcnow)

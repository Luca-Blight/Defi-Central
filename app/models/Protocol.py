from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Protocol(SQLModel, table=True):
    __tablename__ = "protocol"

    id: Optional[int] = Field(default=None, primary_key=True)
    parent_protocol: Optional[str]
    name: Optional[str]
    contract_address: Optional[str]
    symbol: Optional[str]
    category: Optional[str]
    company_url: Optional[str]
    oracle: Optional[str]
    twitter_handle: Optional[str]
    logo: Optional[str]
    created_at: datetime = Field(default=datetime.utcnow)

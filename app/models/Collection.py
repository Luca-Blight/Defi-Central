from sqlalchemy import Column, Integer, String, Enum
from sqlmodel import SQLModel ,Column, Integer, String

import enum


class CurrencyType(enum.Enum):
    """Definition of Brand types"""

    ETH = "ETH"
    WETH = "MATIC"


class Collection(SQLModel, table=True):

    __tablename__ = "collection"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # Types
    name = Column(String(255), nullable=False)

    chain = Column(Enum(CurrencyType))


# Base.metadata.create_all(engine)

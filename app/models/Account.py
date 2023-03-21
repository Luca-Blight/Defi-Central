from sqlalchemy import Column, Integer, String, DateTime, Text

from sqlmodel import Field, SQLModel


class Account(SQLModel, table=True):

    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    account_id = Column(String(255), nullable=False)
    cursor = Column(String(255), nullable=True)
    account_address = Column(String(255), nullable=True)
    block_date = Column(DateTime, nullable=True)
    block_number = Column(Integer, nullable=False)
    transaction_hash = Column(String(255), nullable=True)
    currency = Column(String(64), nullable=True)
    counter = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    contract = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False)


engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
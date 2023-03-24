from database.database import Base

from sqlalchemy import Column, Integer, String, DateTime, Float


class AccountLedger(SQLModel, table=True):
    __tablename__ = "account_ledger"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    account_id = Column(String(255), nullable=False)
    to_account = Column(String(255), nullable=True)
    quantity = Column(Float(), nullable=True)
    currency = Column(String(64), nullable=True)
    from_account = Column(String(255), nullable=False)
    cursor = Column(String(255), nullable=True)
    memo = Column(String(1024), nullable=True)
    transaction_hash = Column(String(255), nullable=False)
    block_date = Column(DateTime, nullable=False)
    block_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)


# Base.metadata.create_all(engine)

from database.database import Base
from sqlmodel import SQLModel, Field, Column, Integer, String, DateTime, ForeignKey


class Raise(SQLModel, table=True):
    __tablename__ = "raise"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    round = Column(String(255), nullable=True)
    amount = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    source = Column(DateTime, nullable=False)
    sector = Column(String(255), nullable=True)
    source = Column(String(255), nullable=True)
    investor_id = Column(Integer, ForeignKey("investor.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)

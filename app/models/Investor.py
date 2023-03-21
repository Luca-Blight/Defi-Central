from database.database import Base
from sqlmodel import SQLModel, Field, Column, Integer, String, DateTime, ForeignKey


class Investor(SQLModel, table=True):

    __tablename__ = "investor"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    fund = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False)

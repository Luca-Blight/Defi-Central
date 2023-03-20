from database import Base
from sqlmodel import SQLModel, Column, Integer, String, DateTime

class Protocol(SQLModel, table=True):

    __tablename__ = "protocol"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    parent_name = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    contract_address = Column(String(255), nullable=True)
    symbol = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    company_url = Column(String(255), nullable=True)
    oracle = Column(String(255), nullable=True)
    twitter_handle = Column(String(255), nullable=True)
    logo = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    
    
# what is treasury?
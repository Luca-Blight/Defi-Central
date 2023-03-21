from sqlmodel import SQLModel, Field
from typing import Optional
from database.database import engine
from datetime import datetime

class Protocol(SQLModel, table=True):
    
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



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def main():
    await create_tables()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
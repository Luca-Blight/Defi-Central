from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, select
from app.models.Financial import Financial
from database.main import async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
import logging


app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname} {message}",
    style="{",
    datefmt="%m-%d-%y %H:%M:%S",
)

log = logging.getLogger()


@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    session = async_session()

    try:
        yield session
    finally:
        await session.close()
        
        
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/tvl/{protocol_id}")
async def get_tvl(protocol_id: int):
    async with get_async_session() as session:
        financial_data = await session.exec(select(Financial).where(Financial.protocol_id == protocol_id))
        log.info(f'financial data: {financial_data}')
        tvl_data = [{"date": data.date, "tvl": data.tvl} for data in financial_data]
        return {"tvl": tvl_data}

@app.get("/fees/{protocol_id}")
async def get_fees():
    return {"message": "Hello World"}


@app.get("/all_tvl/")
async def get_all_tvl():
    return {"message": "Hello World"}


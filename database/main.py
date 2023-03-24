from app.models.Financial import Financial
from app.models.Protocol import Protocol
from sqlalchemy.ext.asyncio import create_async_engine
from config.settings import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_NAME


import asyncio

PG_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_NAME}"

async_engine = create_async_engine(PG_URL, echo=True)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Protocol.metadata.create_all)
        await conn.run_sync(Financial.metadata.create_all)


async def main():
    await create_tables()


if __name__ == "__main__":
    asyncio.run(main())

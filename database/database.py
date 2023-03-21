
from sqlalchemy.ext.asyncio import create_async_engine
from config.settings import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_NAME

PG_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_NAME}"

engine = create_async_engine(PG_URL, echo=True)

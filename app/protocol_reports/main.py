import asyncio
import httpx
import time
import logging
from typing import Coroutine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from database.database import engine
from contextlib import asynccontextmanager


PROTOCOLS = ["yearn-finance", "makerdao", "compound", "dydx", "aave"]


logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname} {message}",
    style="{",
    datefmt="%m-%d-%y %H:%M:%S",
)

log = logging.getLogger()


async def get_protocol(protocol: str):

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(f"https://api.llama.fi/protocol/{protocol}")
        try:
            if (
                response.status_code == 200
                and "application/json" in response.headers["content-type"]
            ):
                return response.json()
            else:
                log.error(
                    f"Error fetching data for {protocol}: {response.status_code}, content-type: {response.headers.get('content-type', 'N/A')}"
                )
                return None
        except httpx.ReadTimeout:
            log.error(f"Read timeout occurred while fetching data for protocol {protocol}")
    return None


async def transform(data: dict) -> dict:

    keys_to_keep = [
        "address",
        "category",
        "logo",
        "name",
        "oracle",
        "parentProtocol",
        "url",
        "symbol",
        "tvl",
        "twitter",
    ]

    result = {key: data.get(key, None) for key in keys_to_keep}

    result["company_url"] = result.pop("url")
    result["contract_address"] = result.pop("address")
    result["parent_protocol"] = result.pop("parentProtocol")
    result["twitter_handle"] = result.pop("twitter")

    return result

    # keys that we want to keep:  address, category, logo, name, url, symbol, treasury, tvl,  twitter,
    # twitter -> twitter_handle, address -> contract_address,

@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    session = async_session()
    
    try:
        yield session
    finally:
        await session.close()


async def load(data: dict):

    (
        category,
        company_url,
        contract_address,
        logo,
        name,
        parent_protocol,
        twitter_handle,
    ) = (
        data["category"],
        data["company_url"],
        data["contract_address"],
        data["logo"],
        data["name"],
        data["parent_protocol"],
        data["twitter_handle"],
    )
    async with get_async_session() as session:
        await session.execute(
            f"INSERT INTO protocol (category, company_url, contract_address,logo, name, parent_protocol, twitter_handle) VALUES ('{category}',  '{contract_address}', '{company_url}', '{logo}','{name}','{parent_protocol}', '{twitter_handle}' ) ON CONFLICT DO NOTHING"
        )
        await session.commit()
        log.info(f"loaded {name} into protocol table")


async def main():

    get_tasks: list[Coroutine] = [
        get_protocol(protocol) for protocol in PROTOCOLS
    ]  # Create coroutines
    task_get_results = await asyncio.gather(
        *get_tasks
    )  # Schedule tasks and execute them concurrently
    task_get_results = [result for result in task_get_results if result is not None]

    transform_tasks: list[Coroutine] = [
        transform(result) for result in task_get_results
    ]
    task_transform_results = await asyncio.gather(*transform_tasks)
    

    load_tasks: list[Coroutine] = [load(result) for result in task_transform_results if result is not None]
    lresults = await asyncio.gather(*load_tasks)


if __name__ == "__main__":
    start = time.time()

    asyncio.run(main())

    end = time.time()

    log.info(f"finished all protocols in {end - start} seconds")


# In this step, we create a list of coroutines by calling the asynchronous function get_protocol for each protocol.
# At this stage, the coroutines are not yet executed, as they are simply scheduled to be run asynchronously.
# These coroutines will be executed concurrently when we use asyncio.gather in the next step (step 5b).


# tvl, top 10

import asyncio
import httpx
import time
import logging

from datetime import timezone
from typing import Coroutine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from database.main import async_engine
from contextlib import asynccontextmanager
from datetime import datetime
from app.models.Protocol import Protocol
from app.models.Financial import Financial
from sqlmodel import select
import requests


# PROTOCOLS = ["yearn-finance", "makerdao", "compound", "dydx", "aave"]


protocols_response = requests.get("https://api.llama.fi/protocols").json()

protocols = [protocol["name"] for protocol in protocols_response]


logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname} {message}",
    style="{",
    datefmt="%m-%d-%y %H:%M:%S",
)

log = logging.getLogger()


async def get_protocol(protocol: str, fees: bool = True):
    async with httpx.AsyncClient(timeout=10) as client:
        response = (
            await client.get(f"https://api.llama.fi/protocol/{protocol}")
            if not fees
            else await client.get(f"https://api.llama.fi/summary/fees/{protocol}")
        )

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
            log.error(
                f"Read timeout occurred while fetching data for protocol {protocol}"
            )
    return None


async def get_protocol_fees(protocol: str):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(f"https://api.llama.fi/summary/fees/{protocol}")

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
            log.error(
                f"Read timeout occurred while fetching data for protocol {protocol}"
            )
    return None


async def transform(data: dict, fees: bool = False) -> dict:
    if fees:
        pass
    else:
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


async def load(data: dict, fees: bool = False):
    if fees:
        async with get_async_session() as session:
            # Retrieve the protocol id from the database and add it to the financial object

            statement = select(Protocol).where(Protocol.name == name)
            existing_protocol = await session.exec(statement)
            existing_protocol = existing_protocol.one()

            for financial in list_of_financials:
                financial.protocol_id = existing_protocol.id
                financial.date = financial.date.astimezone(timezone.utc).replace(
                    tzinfo=None
                )
                statement = select(Financial).where(
                    (Financial.date == financial.date)
                    & (Financial.protocol_id == financial.protocol_id)
                )
                existing_financial = await session.exec(statement)
                existing_financial = existing_financial.one_or_none()

                if existing_financial:
                    existing_financial.tvl = financial.tvl
                    existing_financial.fees = financial.fees
                    await session.commit()
                    log.info(
                        f"Updated financial data for {name} on date {financial.date}"
                    )

    else:
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

        created_at = datetime.utcnow()

        protocol = Protocol(
            category=category,
            company_url=company_url,
            contract_address=contract_address,
            logo=logo,
            name=name,
            parent_protocol=parent_protocol,
            twitter_handle=twitter_handle,
            created_at=created_at,
        )
        async with get_async_session() as session:
            # Check if the protocol already exists in the database, if not, add it

            statement = select(Protocol).where(Protocol.name == name)
            existing_protocol = await session.exec(statement)
            existing_protocol = existing_protocol.one()

            if not existing_protocol:
                session.add(protocol)
                await session.commit()
                log.info(f"Loaded {name} into protocol table")
            else:
                log.info(f"{name} already exists in the protocol table")

        list_of_financials = []

        tvl_data: list[dict] = data["tvl"]

        for financial_data in tvl_data:
            financial_obj = Financial(
                tvl=financial_data["totalLiquidityUSD"],
                date=financial_data["date"],
                created_at=created_at,
            )
            list_of_financials.append(financial_obj)

        async with get_async_session() as session:
            # Retrieve the protocol id from the database and add it to the financial object

            statement = select(Protocol).where(Protocol.name == name)
            existing_protocol = await session.exec(statement)
            existing_protocol = existing_protocol.one()

            for financial in list_of_financials:
                financial.protocol_id = existing_protocol.id
                financial.date = financial.date.astimezone(timezone.utc).replace(
                    tzinfo=None
                )
                statement = select(Financial).where(
                    (Financial.date == financial.date)
                    & (Financial.protocol_id == financial.protocol_id)
                )
                existing_financial = await session.exec(statement)
                existing_financial = existing_financial.one_or_none()

                if not existing_financial:
                    session.add(financial)
                    await session.commit()
                    log.info(
                        f"Loaded financial data for {name} on date {financial.date}"
                    )
                else:
                    log.info(
                        f"Financial data for {name} on date {financial.date} already exists in the financial table"
                    )


async def main(protocols, fees):
    get_tasks: list[Coroutine] = [
        get_protocol(protocol, fees) for protocol in protocols
    ]  # Create coroutines
    task_get_results = await asyncio.gather(
        *get_tasks
    )  # Schedule tasks and execute them concurrently
    task_get_results = [result for result in task_get_results if result is not None]

    transform_tasks: list[Coroutine] = [
        transform(result) for result in task_get_results
    ]
    task_transform_results = await asyncio.gather(*transform_tasks)

    load_tasks: list[Coroutine] = [
        load(result) for result in task_transform_results if result is not None
    ]
    lresults = await asyncio.gather(*load_tasks)


if __name__ == "__main__":
    start = time.time()

    asyncio.run(main(protocols, fees=False))

    end = time.time()

    log.info(f"finished all protocols in {end - start} seconds")

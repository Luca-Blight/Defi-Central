import asyncio
import httpx 
import time
import logging
from typing import Coroutine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession


# raises key -> raise table and/or investor


ASYNC_ENGINE = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/postgres")



PROTOCOLS = ['yearn-finance','makerdao','compound','dydx','aave']

logging.basicConfig(level=logging.INFO, 
                    format="{asctime} {levelname} {message}",
                    style='{',
                    datefmt='%m-%d-%y %H:%M:%S')

log = logging.getLogger()


async def get_protocol(protocol: str):
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://api.llama.fi/protocol/{protocol}')
        if response.status_code == 200 and 'application/json' in response.headers['content-type']:
            return response.json()
        else:
            log.error(f"Error fetching data for {protocol}: {response.status_code}, content-type: {response.headers.get('content-type', 'N/A')}")
            return None

async def transform(data: dict) -> dict:
    
    
    keys_to_keep = ['category', 'logo', 'name', 'url', 'symbol', 'tvl', 'twitter', 'address','oracle', 'parentProtocol']

    result = {key: data.get(key, None) for key in keys_to_keep}
        
    result['company_url'] = result.pop('url')
    result['contract_address'] = result.pop('address')
    result['parent_protocol'] = result.pop('parentProtocol')
    result['twitter_handle'] = result.pop('twitter')

    return result

    # keys that we want to keep:  address, category, logo, name, url, symbol, treasury, tvl,  twitter, 
    # twitter -> twitter_handle, address -> contract_address, 

async def get_async_session() -> AsyncSession:
   async_session = sessionmaker(
       bind=ASYNC_ENGINE, class_=AsyncSession, expire_on_commit=False
   )
   
   async with async_session() as session:
       yield session
       
async def load(data: dict):

    async with get_async_session() as session:
        await session.execute(
            f"INSERT INTO protocol (contract_address, company_url, parent_protocol, twitter_handle) VALUES ('{data['contract_address']}', {data['company_url']}, {data['parent_protocol']}, {data['twitter_handle']} ) ON CONFLICT DO NOTHING"
        )
        await session.commit()

async def main():
    
    
    get_tasks: list[Coroutine] = [get_protocol(protocol) for protocol in PROTOCOLS] # Create coroutines
    task_get_results = await asyncio.gather(*get_tasks) # Schedule tasks and execute them concurrently
    task_get_results = [result for result in task_get_results if result is not None] 
    
    transform_tasks: list[Coroutine] = [transform(result) for result in task_get_results]
    task_transform_results = await asyncio.gather(*transform_tasks)
    
    load_tasks: list[Coroutine] = [load(result) for result in task_transform_results]
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
import aiohttp
import asyncio

from fastapi import FastAPI

from strategies import AverageStrategy, StrategyName


app = FastAPI()
#ENDPOINTS = ['api1.com', 'api2.com', 'api3.com']
ENDPOINTS = ['https://httpbin.org/anything?deductible=1000&stop_loss=10000&oop_max=5000', 'https://httpbin.org/anything?deductible=1200&stop_loss=13000&oop_max=6000', 'https://httpbin.org/anything?deductible=1000&stop_loss=10000&oop_max=6000']


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data.get('args')

async def process_api_endpoints(member_id: int, strategy: object):
    fetch_coroutines = []
    for endpoint in ENDPOINTS:
        url = f'{endpoint}&member_id={member_id}'
        fetch_coroutines.append(asyncio.Task(fetch_url(url)))

    responses = await asyncio.gather(*fetch_coroutines)
    return strategy.process(responses)

@app.get("/")
async def root(member_id: int, strategy: StrategyName=StrategyName.average):
    strategy_instance = None
    if strategy == StrategyName.average:
        strategy_instance = AverageStrategy()

    response = await process_api_endpoints(member_id, strategy_instance)
    return response

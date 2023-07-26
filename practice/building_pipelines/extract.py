import pandas as pd
import sqlite3
from dotenv import load_dotenv
import os 
import asyncio
import aiohttp
from jsonschema import validate, ValidationError
from api_schema import DUNE_API_SCHEMA
from enum import Enum
from typing import Dict, Any, Tuple


load_dotenv()
api_key = os.environ.get('DUNE_API_KEY')

async def fetch_data(session: aiohttp.ClientSession, url: str, name: str) -> Tuple[str, pd.DataFrame]:
    """
    Fetch data asynchronously from the specified URL, validate the response against the DUNE_API_SCHEMA, 
    and transform the response into a DataFrame.

    Args:
        session (aiohttp.ClientSession): An established aiohttp client session for making requests.
        url (str): The URL from where data is to be fetched.
        name (str): The name that is to be assigned to the DataFrame.

    Returns:
        Tuple[str, pd.DataFrame]: A tuple containing name of the DataFrame and the DataFrame itself. 
        In case of validation error or request failure, an empty DataFrame is returned.

    Raises:
        ValidationError: If the response doesn't conform to DUNE_API_SCHEMA.
    """
    async with session.get(url) as response:
        data = await response.json()

        if 'result' in data and 'rows' in data['result']:
            try:
                validate(instance=data, schema=DUNE_API_SCHEMA)
                print(f"Validation successful for {name}. The response JSON data is compliant with the schema.")
                return name, pd.DataFrame(data['result']['rows'])
            except ValidationError as e:
                print(f"Schema error message for {name}:", e)
        else:
            print(f"Request failed with response: {data}.")

        return name, pd.DataFrame()


class ApiQuery(Enum):
    contracts = '2704494'
    active_address = '2704484'
    txn_fee = '2704477'
    eth_price = '2704471'
    eth_burn = '2704461'
    eth_emissions = '2704447'
    
    
class ApiConnection:
    base_url = 'https://api.dune.com/api/v1/query'
    
    def __init__(self, key):
        self.key = api_key


    async def get_data(self) -> Dict[str, pd.DataFrame]:
        """Returns dictionary where key - variable name is a string, correspond to dataframe values
           Avoid need to have dataframes listed linearly
        """
        urls = {f'{query.name}_df': f'{self.base_url}/{query.value}/results?api_key={self.key}' for query in ApiQuery}

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_data(session, url, name) for name, url in urls.items()]
            response_list = await asyncio.gather(*tasks)

        return dict(response_list)
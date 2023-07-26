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

from extract import ApiConnection
from transform import dataframe_conversion 
from load import database_insert


load_dotenv()
api_key = os.environ.get('DUNE_API_KEY')

async def main():
    # establish API connection 
    connection = ApiConnection(api_key)
    # get the data and convert them to dataframes
    dataframes = await connection.get_data()
    # arrange the columns in the dataframes
    arranged_dataframes = dataframe_conversion(dataframes)
    # insert into database
    database_insert(arranged_dataframes)

if __name__ == '__main__':
    asyncio.run(main())
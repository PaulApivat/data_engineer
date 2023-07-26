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

def database_insert(dict_of_df: Dict[str, pd.DataFrame]) -> None:
    """Inserts dataframes into SQLite database"""
    conn = sqlite3.connect('demo.db')
    
    for key, value in dict_of_df.items():
        value.to_sql(name=f'{key}', con=conn, if_exists='replace', index=False)
        print(f"-----{key}--pushed successfully.-----")
    
    conn.close()
    print("Done.")
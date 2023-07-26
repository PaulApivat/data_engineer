
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

def dataframe_conversion(dataframes: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Loops through dictionary of dataframes values, checks if dataframe is empty
       If not, re-arranges column as specified.
       
       Args: Dictionary of dataframe values
       Returns: Dictionary of dataframe values
    """
    df_list = {}

    for name, df in dataframes.items():
        if not df.empty:
            df = df[['day', 'Current', 'Value_7d', 'Performance_7d', 'High_7d', 'Low_7d', 'MA_10d', 'Value_30d', 'Performance_30d', 'High_30d', 'Low_30d', 'MA_50d', 'Value_180d', 'Performance_180d', 'High_180d', 'Low_180d', 'MA_200d']]
            df_list[name] = df
        else:
            print(f"Empty DataFrame for {name}, skipping.")

    return df_list
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch your API key from the environment variables
api_key = os.getenv("DUNE_API_KEY")

dune = DuneClient.from_env()
try:
    results = dune.get_latest_result(3032256, max_age_hours=24)
    print(results)
except Exception as e:
    print(f"Error executing query: {e}")

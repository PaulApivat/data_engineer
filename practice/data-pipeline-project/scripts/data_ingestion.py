import os
import duckdb
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch your API key from the environment variables
api_key = os.getenv("DUNE_API_KEY")

# Define the API endpoint and any necessary parameters
api_url = f"https://api.dune.com/api/v1/query/3032256/results?api_key={api_key}"
params = {"api_key": api_key}

# Make an API request
response = requests.get(api_url, params=params)
print(response)


if response.status_code == 200:
    # Assuming the API response is in JSON format
    data = response.json()
    # print(data["result"]["rows"])

    # Establish a connection to the DuckDB database
    conn = duckdb.connect("data/bronze/raw_data.db")

    # Drop the existing "raw_data" table if it exists
    conn.execute("DROP TABLE IF EXISTS raw_data")

    # Create a DuckDB table with an auto-increment primary key using INTEGER
    conn.execute(
        """
        CREATE TABLE raw_data (
            id INTEGER PRIMARY KEY,
            data STRING
        )
    """
    )

    # Insert the retrieved data into the DuckDB table with auto-incrementing ids
    for idx, item in enumerate(data["result"]["rows"]):
        conn.execute(
            "INSERT INTO raw_data (id, data) VALUES (?, ?)", (idx + 1, json.dumps(item))
        )

    # Close the DuckDB connection
    conn.close()
else:
    print("API request failed with status code:", response.status_code)

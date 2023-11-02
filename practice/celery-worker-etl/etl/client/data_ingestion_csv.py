import os
import sqlite3
import requests
import pandas as pd
from dotenv import load_dotenv
from io import StringIO

# Load environment variables from .env file
load_dotenv()

# Fetch your API key from the environment variables
api_key = os.getenv("DUNE_API_KEY_TEAM")

# Define the API endpoint and any necessary parameters
query_id = 3091796  # without params
api_url = f"https://api.dune.com/api/v1/query/{query_id}/results/csv?api_key={api_key}"

# Define column names for the SQLite table
column_names = [
    "datetime",
    "fees_usd",
    "fees_usd_1w_ago",
    "fees_usd_1w_change",
    "fees_usd_4w_ago",
    "fees_usd_4w_change",
    "fees_usd_26w_ago",
    "fees_usd_26w_change",
    "avg_fees_usd_4w",
    "avg_fees_usd_26w",
    "max_fees_usd_4w",
    "min_fees_usd_4w",
    "max_fees_usd_26w",
    "min_fees_usd_26w",
]

# Make an API request
response = requests.get(api_url)

if response.status_code == 200:
    # Assuming the API response is in CSV format
    data_csv = response.text

    # Use StringIO to convert CSV data into a DataFrame
    df = pd.read_csv(StringIO(data_csv))
    print("print df...", df)

    # Establish a connection to the SQLite database (creating it if not exists)
    db_path = "raw_bronze.db"
    conn = sqlite3.connect(db_path)

    # Create a SQLite table with the specified column data types
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS eth_fees_csv (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TIMESTAMP,
            fees_usd REAL,
            fees_usd_1w_ago REAL,
            fees_usd_1w_change REAL,
            fees_usd_4w_ago REAL,
            fees_usd_4w_change REAL,
            fees_usd_26w_ago REAL,
            fees_usd_26w_change REAL,
            avg_fees_usd_4w REAL,
            avg_fees_usd_26w REAL,
            max_fees_usd_4w REAL,
            min_fees_usd_4w REAL,
            max_fees_usd_26w REAL,
            min_fees_usd_26w REAL
        )
        """
    )

    # Insert the data from the DataFrame into the SQLite table
    for _, row in df.iterrows():
        conn.execute(
            "INSERT INTO eth_fees_csv (datetime, fees_usd, fees_usd_1w_ago, fees_usd_1w_change, fees_usd_4w_ago, fees_usd_4w_change, fees_usd_26w_ago, fees_usd_26w_change, avg_fees_usd_4w, avg_fees_usd_26w, max_fees_usd_4w, min_fees_usd_4w, max_fees_usd_26w, min_fees_usd_26w) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple(row[:14]),  # Exclude the additional fields
        )

    # Commit changes and close the SQLite connection
    conn.commit()
    conn.close()

    print(f"Data inserted into {db_path}")
else:
    print("API request failed with status code:", response.status_code)

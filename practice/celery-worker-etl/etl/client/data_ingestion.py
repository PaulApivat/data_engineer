import os
import sqlite3
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch your API key from the environment variables
api_key = os.getenv("DUNE_API_KEY_TEAM")

# Define the API endpoint and any necessary parameters
query_id = 3091796  # without params
api_url = f"https://api.dune.com/api/v1/query/{query_id}/results?api_key={api_key}"

# Define column names for the SQLite table
column_names = ['datetime', 'fees_usd', 'fees_usd_1w_ago', 'fees_usd_1w_change', 'fees_usd_4w_ago', 'fees_usd_4w_change', 'fees_usd_26w_ago', 'fees_usd_26w_change', 'avg_fees_usd_4w', 'avg_fees_usd_26w', 'max_fees_usd_4w', 'min_fees_usd_4w', 'max_fees_usd_26w', 'min_fees_usd_26w']


# Make an API request
response = requests.get(api_url)

if response.status_code == 200:
    # Assuming the API response is in JSON format
    data = response.json()

    # Transform the JSON data into a DataFrame
    df = pd.DataFrame(data["result"]["rows"], columns=column_names)

    # Establish a connection to the SQLite database (creating it if not exists)
    db_path = "raw_bronze.db"
    conn = sqlite3.connect(db_path)

    # Create a SQLite table with the specified column data types
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS eth_fees (
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
            min_fees_usd_26w REAL,
            project_name TEXT,
            project_symbol TEXT,
            project_category TEXT
        )
    """
    )

    # Insert the data from the DataFrame into the SQLite table
    for _, row in df.iterrows():
        # Add project details to each row
        row = row.tolist()
        row.extend(["Ethereum", "ETH", "L1"])  # Modify project details as needed
        conn.execute(
            "INSERT INTO eth_fees (datetime, fees_usd, fees_usd_1w_ago, fees_usd_1w_change, fees_usd_4w_ago, fees_usd_4w_change, fees_usd_26w_ago, fees_usd_26w_change, avg_fees_usd_4w, avg_fees_usd_26w, max_fees_usd_4w, min_fees_usd_4w, max_fees_usd_26w, min_fees_usd_26w, project_name, project_symbol, project_category) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple(row),
        )

    # Commit changes and close the SQLite connection
    conn.commit()
    conn.close()

    print(f"Data inserted into {db_path}")
else:
    print("API request failed with status code:", response.status_code)
import os
import sqlite3
import requests
import pandas as pd
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

    # Transform the JSON data into a DataFrame
    df = pd.DataFrame(
        data["result"]["rows"],
        columns=["datetime", "net_emission_eth", "total_net_emission_eth"],
    )
    # print(df)

    # Establish a connection to the DuckDB database
    conn = sqlite3.connect("data/bronze/raw_sqlite.db")

    # Drop the existing "raw_data" table if it exists
    conn.execute("DROP TABLE IF EXISTS sample_params")

    # Create a DuckDB table with an auto-increment primary key using INTEGER
    # Create a DuckDB table with the specified column data types
    conn.execute(
        """
        CREATE TABLE sample_params (
            datetime TIMESTAMP,
            net_emission_eth FLOAT,
            total_net_emission_eth FLOAT
        )
    """
    )

    # Insert the data from the DataFrame into the DuckDB table
    for _, row in df.iterrows():
        try:
            conn.execute(
                "INSERT INTO sample_params (datetime, net_emission_eth, total_net_emission_eth) VALUES (?, ?, ?)",
                (
                    row["datetime"],
                    row["net_emission_eth"],
                    row["total_net_emission_eth"],
                ),
            )
            print(row)
        except Exception as e:
            print(f"Error inserting row: {row}\nError message: {e}")

    # commit the change to SQLite
    conn.commit()

    # Close the DuckDB connection
    conn.close()
else:
    print("API request failed with status code:", response.status_code)

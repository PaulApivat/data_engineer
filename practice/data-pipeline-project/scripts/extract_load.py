import os
import requests
import sqlite3
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch your API key from the environment variables
api_key = os.getenv("DUNE_API_KEY")

# Define the API endpoint and any necessary parameters
api_url = f"https://api.dune.com/api/v1/query/3034904/results?api_key={api_key}"  # Query: @m0xt - Blockchain_users_new
params = {"api_key": api_key}

# Make an API request
response = requests.get(api_url, params=params)
print("API Response :", response)

# print("JSON blob :", response.json())

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    json_data = response.json()

    # Convert the JSON blob to a DataFrame
    # df = pd.DataFrame(json_data)
    df = pd.DataFrame(json_data["result"]["rows"])

    print("COLUMN ORDER :", df.columns)

    # Connect to the SQLite database
    db_path = "data/bronze/user_bronze.db"  # Database file name
    conn = sqlite3.connect(db_path)

    # Replace the table if it exists, or create a new one
    # columns parameter preserves ordering to be the same as source API
    df.to_sql("user_raw_2", conn, if_exists="replace", index=False)

    # Close the database connection
    conn.close()

    print("Data saved to SQLite database: user_raw_2 in data/bronze/user_bronze.db")
else:
    print("API request failed with status code:", response.status_code)

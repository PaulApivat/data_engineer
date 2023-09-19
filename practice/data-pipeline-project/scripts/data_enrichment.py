import duckdb

# Connect to the existing database containing the raw data
raw_db_path = "data/bronze/raw_data.db"
conn = duckdb.connect(raw_db_path)

# Query the existing "eth_emissions" table and create the enriched DataFrame
enriched_df = conn.execute(
    """
    SELECT
        datetime,
        net_emission_eth,
        total_net_emission_eth,
        'ETH' AS token_symbol,
        'ethereum' AS protocol,
        'eth overview' AS category,
        'L1' AS layer,
        'ETH supply' AS measure
    FROM eth_emissions
"""
).fetchdf()

# Disconnect from the raw data database
conn.close()
print("connection to data/bronze/raw_data.db successful.")

# Create a new database for the enriched data
silver_db_path = "data/silver/transform_data.db"
conn = duckdb.connect(silver_db_path)


try:
    # Create the "eth_emissions_silver" table in the new database
    conn.execute(
        """
       CREATE TABLE eth_emissions_silver (
           datetime TIMESTAMP,
           net_emission_eth FLOAT,
           total_net_emission_eth FLOAT,
           token_symbol STRING,
           protocol STRING,
           category STRING,
           layer STRING,
           measure STRING
       )
    """
    )
except Exception as e:
    # Handle the exception if the table already exists
    if "Table with name eth_emissions_silver already exists!" in str(e):
        pass

# Insert the enriched data from the DataFrame into the "eth_emissions_silver" table
for _, row in enriched_df.iterrows():
    conn.execute(
        """
        INSERT INTO eth_emissions_silver (datetime, net_emission_eth, total_net_emission_eth, token_symbol, protocol, category, layer, measure)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            row["datetime"],
            row["net_emission_eth"],
            row["total_net_emission_eth"],
            row["token_symbol"],
            row["protocol"],
            row["category"],
            row["layer"],
            row["measure"],
        ),
    )

# Disconnect from the new database
conn.close()
print("creation of enriched table at data/silver/transform_data.db successful.")

import duckdb

# Step 1: Create a new database for consumption data (data/gold/consumption_data.db)
dest_db_path = "data/gold/consumption_data.db"
dest_conn = duckdb.connect(dest_db_path)

# Step 2: Drop the existing eth_emissions_gold table (if it exists)
try:
    dest_conn.execute("DROP TABLE IF EXISTS eth_emissions_gold")
except Exception as e:
    # Handle exceptions if there are any issues with dropping the table
    print(f"Error dropping existing eth_emissions_gold table: {e}")

# Step 2: Create a new table inside consumption_data.db (eth_emissions_gold)
try:
    dest_conn.execute(
        """
    CREATE TABLE IF NOT EXISTS eth_emissions_gold (
        datetime TIMESTAMP,
        total REAL,
        total_7d REAL,
        pct_change_total_7d REAL,
        wk REAL,
        past_wk_7d REAL,
        pct_change_past_wk_7d REAL,
        past_wk_30d REAL,
        pct_change_past_wk_30d REAL,
        past_wk_180d REAL,
        pct_change_past_wk_180d REAL
    )
    """
    )
except Exception as e:
    # Handle exceptions if the table already exists or any other issues
    print(f"Error creating eth_emissions_gold table: {e}")

# Disconnect from the destination database
dest_conn.close()
print("Step 2: Table eth_emissions_gold created successfully.")

# Step 3: Connect to the existing database (data/silver/transform_data.db)
source_db_path = "data/silver/transform_data.db"
source_conn = duckdb.connect(source_db_path)

# Step 4: Query from the existing table eth_emissions_silver and create a new DataFrame
source_query = """
SELECT
    datetime,
    total_net_emission_eth AS total,
    TRY_CAST(LAG(total_net_emission_eth, 7) OVER (ORDER BY datetime ASC) AS REAL) AS total_7d,
    TRY_CAST((total_net_emission_eth - LAG(total_net_emission_eth, 7) OVER (ORDER BY datetime ASC)) / LAG(total_net_emission_eth, 7) OVER (ORDER BY datetime ASC) AS REAL) AS pct_change_total_7d,
    TRY_CAST(SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS REAL) AS wk,
    TRY_CAST(SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 13 PRECEDING AND 7 PRECEDING) AS REAL) AS past_wk_7d,
    TRY_CAST((SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) - SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 13 PRECEDING AND 7 PRECEDING)) / SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 13 PRECEDING AND 7 PRECEDING) AS REAL) AS pct_change_past_wk_7d,
    TRY_CAST(SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 36 PRECEDING AND 30 PRECEDING) AS REAL) AS past_wk_30d,
    TRY_CAST((SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) - SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 36 PRECEDING AND 30 PRECEDING)) / SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 36 PRECEDING AND 30 PRECEDING) AS REAL) AS pct_change_past_wk_30d,
    TRY_CAST(SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 186 PRECEDING AND 180 PRECEDING) AS REAL) AS past_wk_180d,
    TRY_CAST((SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) - SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 186 PRECEDING AND 180 PRECEDING)) / SUM(net_emission_eth) OVER (ORDER BY datetime ASC ROWS BETWEEN 186 PRECEDING AND 180 PRECEDING) AS REAL) AS pct_change_past_wk_180d
FROM eth_emissions_silver
"""

# Step 5: Execute the query and create a new DataFrame
source_df = source_conn.execute(source_query).fetchdf()
source_df_sorted = source_df.sort_values(by="datetime", ascending=False)
print(source_df_sorted)

# Step 6: Disconnect from the source database
source_conn.close()
print("Step 6: Disconnected from the source database.")

# Step 7: Connect to the destination database (again)
dest_conn = duckdb.connect(dest_db_path)

# Step 8: Sort the source DataFrame by datetime in descending order


# Step 9: Insert the sorted DataFrame into eth_emissions_gold table
for _, row in source_df_sorted.iterrows():
    try:
        dest_conn.execute(
            """
            INSERT INTO eth_emissions_gold
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["datetime"],
                row["total"],
                row["total_7d"],
                row["pct_change_total_7d"],
                row["wk"],
                row["past_wk_7d"],
                row["pct_change_past_wk_7d"],
                row["past_wk_30d"],
                row["pct_change_past_wk_30d"],
                row["past_wk_180d"],
                row["pct_change_past_wk_180d"],
            ),
        )
    except Exception as e:
        # Handle exceptions if there are any issues with insertion
        print(f"Error inserting row: {e}")


# Step 10: Print successful insertion statement
print("Data inserted successfully into eth_emissions_gold table.")

# Disconnect from the destination database
dest_conn.close()
print("Step 11: Disconnected from the destination database.")

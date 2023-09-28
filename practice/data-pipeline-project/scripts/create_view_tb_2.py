import sqlite3

# Connect to the SQLite database
db_path = "data/bronze/user_bronze.db"
conn = sqlite3.connect(db_path)

# Define the name of the view and table
view_name = "user_chart_view"
fact_table = "user_raw_fact"
dim_table = "user_blockchain_dim"

# Create the view with a JOIN between the fact and dimension tables
create_view_query = f"""
CREATE VIEW IF NOT EXISTS {view_name} AS
SELECT {fact_table}.datetime, {fact_table}.weekly_users_count, {dim_table}.blockchain
FROM {fact_table}
INNER JOIN {dim_table} ON {fact_table}.blockchain_id = {dim_table}.blockchain_id
"""

conn.execute(create_view_query)
conn.commit()

# Close the database connection
conn.close()

print(f"View '{view_name}' created with the specified columns.")

import sqlite3

# Connect to the SQLite database
db_path = "data/bronze/user_bronze.db"
conn = sqlite3.connect(db_path)

# Define the names of the source table and view
source_table = "user_raw_fact"
view_name = "user_llm_view"

# Create the view to select the most recent rows
create_view_query = f"""
CREATE VIEW IF NOT EXISTS {view_name} AS
SELECT t1.*
FROM {source_table} AS t1
INNER JOIN (
    SELECT blockchain_id, MAX(datetime) AS max_datetime
    FROM {source_table}
    GROUP BY blockchain_id
) AS t2 ON t1.blockchain_id = t2.blockchain_id AND t1.datetime = t2.max_datetime
"""

conn.execute(create_view_query)
conn.commit()

# Close the database connection
conn.close()

print(
    f"View '{view_name}' created to select the most recent rows based on distinct blockchain_id."
)

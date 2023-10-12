import sqlite3

# Connect to the SQLite database (use the correct path to your "raw_bronze.db" database)
db_path = "raw_bronze.db"
conn = sqlite3.connect(db_path)

# Define the names of the source table and view
source_table = "eth_fees"
view_name = "eth_fees_llm_view"

# Create the view to select the most recent rows
create_view_query = f"""
CREATE VIEW IF NOT EXISTS {view_name} AS
SELECT t1.*
FROM {source_table} AS t1
INNER JOIN (
    SELECT MAX(datetime) AS max_datetime
    FROM {source_table}
) AS t2 ON t1.datetime = t2.max_datetime
"""

conn.execute(create_view_query)
conn.commit()

# Define a test query to retrieve data from the view
test_query = f"SELECT * FROM {view_name}"

# Execute the test query and print the results
cursor = conn.execute(test_query)
for row in cursor.fetchall():
    print(row)

# Close the database connection
conn.close()

print(f"View '{view_name}' created to select the most recent rows based on datetime.")

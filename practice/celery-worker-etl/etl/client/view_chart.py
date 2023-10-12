import sqlite3
import pandas as pd

# Connect to the SQLite database (use the correct path to your "raw_bronze.db" database)
db_path = "raw_bronze.db"
conn = sqlite3.connect(db_path)

# Define the names of the source table and view
source_table = "eth_fees"
view_name = "eth_fees_chart_view"

# Create the view to select specific columns
create_view_query = f"""
CREATE VIEW IF NOT EXISTS {view_name} AS
SELECT datetime, fees_usd, project_name
FROM {source_table}
"""

# Execute the create view query
conn.execute(create_view_query)
conn.commit()

# Define a test query to retrieve data from the view
test_query = f"SELECT * FROM {view_name}"

# Execute the test query and convert the result into a DataFrame
df = pd.read_sql_query(test_query, conn)

# Close the database connection
conn.close()

# Print the DataFrame
print(df)

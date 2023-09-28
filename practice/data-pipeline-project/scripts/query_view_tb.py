import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = "data/bronze/user_bronze.db"
conn = sqlite3.connect(db_path)

# Define the name of the view
view_name = "user_llm_view"

# Define second view
chart_view_name = "user_chart_view"

# Query the view to retrieve the most recent rows based on distinct blockchain_id values
query = f"""
SELECT *
FROM {view_name}
"""

query_2 = f"""
SELECT * 
FROM {chart_view_name}
"""

# Execute the query and fetch the results into a DataFrame
df = pd.read_sql_query(query, conn)
print(df)

print("\n")

df_2 = pd.read_sql_query(query_2, conn)
print(df_2)

# Execute the query and fetch the results
# result = conn.execute(query)

# Print the query results
# for row in result.fetchall():
#     print(row)

# Close the database connection
conn.close()

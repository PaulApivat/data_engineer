import sqlite3

# Connect to the SQLite database
db_path = "data/bronze/user_bronze.db"
conn = sqlite3.connect(db_path)

# Define the table names
source_table = "user_raw_2"
destination_table = "user_raw_fact"

# Define the desired column order
desired_columns = [
    "datetime",
    "blockchain",
    "total_users",
    "total_users_7d",
    "pct_change_total_users_7d",
    "weekly_users_count",
    "weekly_users_count_7d_ago",
    "pct_change_weekly_users_count_vs_7d_ago",
    "weekly_users_count_30d_ago",
    "pct_change_weekly_users_count_vs_30d_ago",
    "weekly_users_count_180d_ago",
    "pct_change_weekly_users_count_vs_180d_ago",
    "avg_weekly_users_30d",
    "avg_weekly_users_180d",
    "max_weekly_users_30d",
    "min_weekly_users_30d",
    "max_weekly_users_180d",
    "min_weekly_users_180d",
]

# Create the destination table with the desired column order
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {destination_table} AS
SELECT {', '.join(desired_columns)}
FROM {source_table}
"""

conn.execute(create_table_query)
conn.commit()

# Close the database connection
conn.close()

print(f"Table '{destination_table}' created with the desired column order.")

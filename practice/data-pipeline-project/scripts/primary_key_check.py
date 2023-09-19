import duckdb

# Connect to the database containing the table
db_path = "data/silver/transform_data.db"
conn = duckdb.connect(db_path)

# Specify the table name
table_name = "eth_emissions_silver"

# Query the system catalog to check for primary key constraints
result = conn.execute(
    f"SELECT * FROM sqlite_master WHERE type='table' AND name='{table_name}'"
)

# Check if the table exists and has a primary key
for row in result.fetchall():
    if "PRIMARY KEY" in row[4]:
        print(f"The table '{table_name}' has a PRIMARY KEY constraint.")
        break
else:
    print(f"The table '{table_name}' does not have a PRIMARY KEY constraint.")

# Disconnect from the database
conn.close()

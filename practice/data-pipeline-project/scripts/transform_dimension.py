import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = "data/bronze/user_bronze.db"
conn = sqlite3.connect(db_path)

# Extract unique values from the "blockchain" column in your Fact Table
query = "SELECT DISTINCT blockchain FROM user_raw_2"
unique_blockchains = conn.execute(query).fetchall()

# Create a DataFrame with unique values
df_blockchains = pd.DataFrame(unique_blockchains, columns=["blockchain"])

# Add a surrogate key column
df_blockchains["blockchain_id"] = df_blockchains.reset_index().index + 1

# Create the Dimension Table "user_blockchain_dim"
df_blockchains.to_sql("user_blockchain_dim", conn, if_exists="replace", index=False)

# Add a foreign key to your Fact Table
# Replace "your_fact_table_name" with the actual name of your Fact Table
query = f"""
ALTER TABLE user_raw_2
ADD COLUMN blockchain_id INTEGER
"""
conn.execute(query)

# Add the foreign key constraint
query = f"""
UPDATE user_raw_2
SET blockchain_id = (SELECT blockchain_id FROM user_blockchain_dim WHERE user_blockchain_dim.blockchain = user_raw_2.blockchain)
"""
conn.execute(query)

# Commit changes and close the database connection
conn.commit()
conn.close()

print(
    "Dimension Table 'user_blockchain_dim' created and linked to the Fact Table: user_raw_2."
)

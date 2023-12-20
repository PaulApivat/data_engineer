import sqlite3

# Define the path to your SQLite database
# db_path = "etl/common/model/db/bronze.db"
db_path = "rocketpool.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Drop the date_dimension table
    cursor.execute("DROP TABLE IF EXISTS protocol_users_pages")

    # Commit the changes to the database
    conn.commit()
    print("protocol_users_pages table dropped successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

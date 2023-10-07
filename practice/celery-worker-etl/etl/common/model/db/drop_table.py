import sqlite3

# Define the path to your SQLite database
db_path = "etl/common/model/db/bronze.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Drop the date_dimension table
    cursor.execute("DROP TABLE IF EXISTS digital_asset_metric")

    # Commit the changes to the database
    conn.commit()
    print("digital_asset_metric table dropped successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

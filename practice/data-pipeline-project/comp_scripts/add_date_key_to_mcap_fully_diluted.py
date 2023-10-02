import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Add the "date_key" column to the mcap_fully_diluted table
    cursor.execute(
        """
        ALTER TABLE mcap_fully_diluted
        ADD COLUMN date_key INTEGER
        """
    )

    # Commit the changes to the database
    conn.commit()
    print("Column 'date_key' added to mcap_fully_diluted table successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

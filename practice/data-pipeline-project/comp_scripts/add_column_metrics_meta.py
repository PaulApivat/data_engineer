import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Add the "data_source" column to metrics_meta if it doesn't exist
    cursor.execute(
        """
        ALTER TABLE metrics_meta
        ADD COLUMN data_source TEXT DEFAULT 'token_terminal'
        """
    )

    # Commit the changes to the database
    conn.commit()
    print("data_source column added to metrics_meta successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Insert data from mcap_fully_diluted into mcap_change
    cursor.execute(
        """
        INSERT INTO mcap_change (datetime, value, project, date_key)
        SELECT datetime, value, project, date_key
        FROM mcap_fully_diluted
        """
    )

    # Commit the changes to the database
    conn.commit()
    print("Data copied from 'mcap_fully_diluted' to 'mcap_change' table successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Convert the "datetime" column in the mcap_fully_diluted table to SMALLDATETIME format
    cursor.execute(
        """
        UPDATE mcap_fully_diluted
        SET datetime = (
            SELECT strftime('%Y-%m-%d %H:%M:%S', datetime(mcap_fully_diluted.datetime))
        )
        WHERE mcap_fully_diluted.datetime IS NOT NULL
        """
    )

    # Update the "date_key" column in the mcap_fully_diluted table based on the join with date_dimension
    cursor.execute(
        """
        UPDATE mcap_fully_diluted AS m
        SET date_key = (
            SELECT date_dimension.date_key
            FROM date_dimension
            WHERE date(m.datetime) = date(date_dimension.full_date)
        )
        WHERE m.datetime IS NOT NULL
        """
    )

    # Commit the changes to the database
    conn.commit()
    print(
        "datetime columns converted and date_key column added and updated in mcap_fully_diluted table successfully!"
    )

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

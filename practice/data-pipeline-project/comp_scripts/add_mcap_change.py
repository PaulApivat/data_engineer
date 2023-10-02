import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Calculate and update change_180d and change_90d columns in mcap_change
    cursor.execute(
        """
        UPDATE mcap_change AS m
        SET
            change_180d = (
                SELECT (m.value - prev180.value) AS change_180d
                FROM mcap_change AS prev180
                WHERE m.project = prev180.project
                    AND m.date_key = (prev180.date_key + 180)
            ),
            change_90d = (
                SELECT (m.value - prev90.value) AS change_90d
                FROM mcap_change AS prev90
                WHERE m.project = prev90.project
                    AND m.date_key = (prev90.date_key + 90)
            )
        """
    )

    # Commit the changes to the database
    conn.commit()
    print(
        "Changes in 'value' column over the past 180 days and 90 days calculated and updated in 'mcap_change' table successfully!"
    )

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

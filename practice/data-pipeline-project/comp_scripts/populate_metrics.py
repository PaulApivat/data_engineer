import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Disable foreign key constraint temporarily
    conn.execute("PRAGMA foreign_keys=OFF;")

    # Populate the metric_id column in metrics with integers
    cursor.execute(
        """
        UPDATE metrics
        SET metric_id = (SELECT COUNT(*) FROM metrics AS m2 WHERE m2.rowid <= metrics.rowid)
        WHERE metric_id IS NULL
    """
    )

    # Commit the changes to the database
    conn.commit()
    print("metric_id populated in metrics successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Re-enable foreign key constraint
    conn.execute("PRAGMA foreign_keys=ON;")

    # Close the database connection
    conn.close()

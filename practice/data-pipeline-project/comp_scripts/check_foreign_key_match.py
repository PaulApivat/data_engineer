import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Update the metrics table to match the category values in metrics_meta
    cursor.execute(
        """
        UPDATE metrics
        SET category = (SELECT category FROM metrics_meta WHERE metrics_meta.category = metrics.category)
    """
    )

    # Commit the changes to the database
    conn.commit()
    print("Category values in the metrics table updated successfully.")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

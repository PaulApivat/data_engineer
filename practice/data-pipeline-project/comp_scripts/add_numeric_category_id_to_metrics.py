import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Add the "numeric_category_id" column to metrics if it doesn't exist
    cursor.execute(
        """
        ALTER TABLE metrics
        ADD COLUMN numeric_category_id INTEGER
        """
    )

    # Update the numeric_category_id column in metrics based on metric_id from metric_key
    cursor.execute(
        """
        UPDATE metrics
        SET numeric_category_id = (
            SELECT numeric_category_id
            FROM metric_key
            WHERE metric_key.metric_id = metrics.metric_id
        )
        WHERE metric_id IN (
            SELECT metric_id
            FROM metric_key
        )
        """
    )

    # Commit the changes to the database
    conn.commit()
    print("numeric_category_id column added to metrics and updated successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

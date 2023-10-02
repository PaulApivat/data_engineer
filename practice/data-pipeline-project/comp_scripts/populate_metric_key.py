import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Disable foreign key constraint temporarily
    conn.execute("PRAGMA foreign_keys=OFF;")

    # Drop the existing metric_key table if it exists
    cursor.execute("DROP TABLE IF EXISTS metric_key")

    # Create a new metric_key table with correct associations
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS metric_key (
            category_id INTEGER,
            metric_id INTEGER,
            metric_name TEXT,
            FOREIGN KEY (category_id) REFERENCES metrics_meta(category_id),
            FOREIGN KEY (metric_id) REFERENCES metrics(metric_id)
        )
        """
    )

    # Populate the metric_key table with data from metrics_meta and metrics
    cursor.execute(
        """
        INSERT INTO metric_key (category_id, metric_id, metric_name)
        SELECT mm.category_id, m.metric_id, m.metric
        FROM metrics m
        JOIN metrics_meta mm ON m.category = mm.category
        """
    )

    # Commit the changes to the database
    conn.commit()
    print("metric_key table recreated successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Re-enable foreign key constraint
    conn.execute("PRAGMA foreign_keys=ON;")

    # Close the database connection
    conn.close()

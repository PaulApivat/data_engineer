import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Disable foreign key constraint temporarily
    conn.execute("PRAGMA foreign_keys=OFF;")

    # Add the metric_id column to metrics_meta if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS metrics_meta (
            category_id INTEGER PRIMARY KEY,
            category TEXT,
            definition TEXT
        )
    """
    )

    # Add the metric_id column to metrics if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS metrics (
            metric_id INTEGER PRIMARY KEY,
            category_id INTEGER,
            metric TEXT
        )
    """
    )

    # Create a new table to store the surrogate keys and associations
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS metric_key (
            metric_id INTEGER PRIMARY KEY,
            category_id INTEGER,
            metric_name TEXT,
            FOREIGN KEY (category_id) REFERENCES metrics_meta(category_id)
        )
    """
    )

    # Populate the metric_key table with data from metrics and metrics_meta
    cursor.execute(
        """
        INSERT INTO metric_key (category_id, metric_name)
        SELECT mm.category_id AS category_id, m.metric AS metric_name
        FROM metrics m
        JOIN metrics_meta mm ON m.category = mm.category
    """
    )

    # Commit the changes to the database
    conn.commit()
    print("Surrogate keys and associations created successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Re-enable foreign key constraint
    conn.execute("PRAGMA foreign_keys=ON;")

    # Close the database connection
    conn.close()

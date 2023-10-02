import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Disable foreign key constraint temporarily
    conn.execute("PRAGMA foreign_keys=OFF;")

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

    # Populate the category_id column in metrics_meta with integers
    cursor.execute(
        """
        UPDATE metrics_meta
        SET category_id = CASE
            WHEN category = 'market data' THEN 1
            WHEN category = 'gmv data' THEN 2
            WHEN category = 'financial data' THEN 3
            WHEN category = 'valuation data' THEN 4
            WHEN category = 'alternative data' THEN 5
            WHEN category = 'cash management data' THEN 6
            ELSE NULL
        END
        WHERE category_id IS NULL
    """
    )

    # Commit the changes to the database
    conn.commit()
    print("category_id populated in metrics_meta successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Re-enable foreign key constraint
    conn.execute("PRAGMA foreign_keys=ON;")

    # Close the database connection
    conn.close()

import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Add the "numeric_category" column to metric_key if it doesn't exist
    cursor.execute(
        """
        ALTER TABLE metric_key
        ADD COLUMN numeric_category TEXT
        """
    )

    # Add the "numeric_category_id" column to metric_key if it doesn't exist
    cursor.execute(
        """
        ALTER TABLE metric_key
        ADD COLUMN numeric_category_id INTEGER
        """
    )

    # Define the mappings of metric_ids to numeric categories
    additive_metrics = [16, 17, 18, 19, 20, 21, 22, 29, 30, 31, 32, 34, 36]
    non_additive_metrics = [1, 2, 4, 5, 6, 7, 14, 23, 24, 25, 26, 33, 37]
    tbd_metrics = [3, 8, 9, 10, 11, 12, 13, 15, 35]

    # Update the numeric_category and numeric_category_id columns based on metric_id
    for metric_id in additive_metrics:
        cursor.execute(
            """
            UPDATE metric_key
            SET numeric_category = 'additive',
                numeric_category_id = 1
            WHERE metric_id = ?
            """,
            (metric_id,),
        )

    for metric_id in non_additive_metrics:
        cursor.execute(
            """
            UPDATE metric_key
            SET numeric_category = 'non_additive',
                numeric_category_id = 2
            WHERE metric_id = ?
            """,
            (metric_id,),
        )

    for metric_id in tbd_metrics:
        cursor.execute(
            """
            UPDATE metric_key
            SET numeric_category = 'tbd',
                numeric_category_id = 3
            WHERE metric_id = ?
            """,
            (metric_id,),
        )

    # Commit the changes to the database
    conn.commit()
    print(
        "Columns numeric_category and numeric_category_id added to metric_key and updated successfully!"
    )

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

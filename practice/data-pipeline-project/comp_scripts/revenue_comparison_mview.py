import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Create a table for revenue comparison
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS revenue_comparison (
            month_name TEXT,
            polygon_revenue REAL,
            op_mainnet_revenue REAL,
            arbitrum_revenue REAL
        )
        """
    )

    # Insert data into the revenue_comparison table
    cursor.execute(
        """
        INSERT INTO revenue_comparison (month_name, polygon_revenue, op_mainnet_revenue, arbitrum_revenue)
        SELECT
            date_dimension.month_name,
            SUM(CASE WHEN revenue.project = 'polygon' THEN revenue.value ELSE 0 END) AS polygon_revenue,
            SUM(CASE WHEN revenue.project = 'op mainnet' THEN revenue.value ELSE 0 END) AS op_mainnet_revenue,
            SUM(CASE WHEN revenue.project = 'arbitrum' THEN revenue.value ELSE 0 END) AS arbitrum_revenue
        FROM
            revenue
        JOIN
            date_dimension ON revenue.date_key = date_dimension.date_key
        WHERE
            date_dimension.year BETWEEN 2021 AND 2022
        GROUP BY
            date_dimension.month_name
        """
    )

    # Commit the changes to the database
    conn.commit()
    print("Table 'revenue_comparison' created and populated successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

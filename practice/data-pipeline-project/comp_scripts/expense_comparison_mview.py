import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Create a table for weekday expense comparison
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weekday_expense_comparison (
            day_name TEXT,
            polygon_expense REAL,
            op_mainnet_expense REAL,
            arbitrum_expense REAL
        )
        """
    )

    # Populate data into the weekday_expense_comparison table
    cursor.execute(
        """
        INSERT INTO weekday_expense_comparison (day_name, polygon_expense, op_mainnet_expense, arbitrum_expense)
        SELECT
            date_dimension.day_name,
            SUM(CASE WHEN expenses.project = 'polygon' AND date_dimension.weekday_flag = 'Weekday' THEN expenses.value ELSE 0 END) AS polygon_expense,
            SUM(CASE WHEN expenses.project = 'op mainnet' AND date_dimension.weekday_flag = 'Weekday' THEN expenses.value ELSE 0 END) AS op_mainnet_expense,
            SUM(CASE WHEN expenses.project = 'arbitrum' AND date_dimension.weekday_flag = 'Weekday' THEN expenses.value ELSE 0 END) AS arbitrum_expense
        FROM
            expenses
        JOIN
            date_dimension ON expenses.date_key = date_dimension.date_key
        WHERE
            date_dimension.full_date BETWEEN date('now', '-365 days') AND date('now')
        GROUP BY
            date_dimension.day_name
        """
    )

    # Commit the changes to the database
    conn.commit()
    print("Table 'weekday_expense_comparison' created and populated successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

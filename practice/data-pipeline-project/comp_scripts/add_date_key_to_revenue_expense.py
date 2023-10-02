import sqlite3

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Convert the "datetime" column in the revenue table to SMALLDATETIME format
    cursor.execute(
        """
        UPDATE revenue
        SET datetime = (
            SELECT strftime('%Y-%m-%d %H:%M:%S', datetime(revenue.datetime))
        )
        WHERE revenue.datetime IS NOT NULL
        """
    )

    # Convert the "datetime" column in the expenses table to SMALLDATETIME format
    cursor.execute(
        """
        UPDATE expenses
        SET datetime = (
            SELECT strftime('%Y-%m-%d %H:%M:%S', datetime(expenses.datetime))
        )
        WHERE expenses.datetime IS NOT NULL
        """
    )

    # Update the "date_key" column in the revenue table based on the join with date_dimension
    cursor.execute(
        """
        UPDATE revenue AS r
        SET date_key = (
            SELECT date_dimension.date_key
            FROM date_dimension
            WHERE date(r.datetime) = date(date_dimension.full_date)
        )
        WHERE r.datetime IS NOT NULL
        """
    )

    # Update the "date_key" column in the expenses table based on the join with date_dimension
    cursor.execute(
        """
        UPDATE expenses AS e
        SET date_key = (
            SELECT date_dimension.date_key
            FROM date_dimension
            WHERE date(e.datetime) = date(date_dimension.full_date)
        )
        WHERE e.datetime IS NOT NULL
        """
    )

    # Commit the changes to the database
    conn.commit()
    print(
        "datetime columns converted and date_key column updated in revenue and expenses tables successfully!"
    )

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

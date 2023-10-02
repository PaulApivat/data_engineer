import sqlite3
import datetime

# Define the path to your SQLite database
db_path = "data/bronze/comp_db_2.db"

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Create the date_dimension table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS date_dimension (
            date_key SMALLINT NOT NULL,
            full_date SMALLDATETIME,
            day_of_week TINYINT,
            day_num_in_month TINYINT,
            day_num_overall SMALLINT,
            day_name VARCHAR(9),
            day_abbrev CHAR(3),
            weekday_flag CHAR(1),
            week_num_in_year TINYINT,
            week_num_overall SMALLINT,
            week_begin_date SMALLDATETIME,
            week_begin_date_key SMALLINT,
            month TINYINT,
            month_num_overall SMALLINT,
            month_name VARCHAR(9),
            month_abbrev CHAR(3),
            quarter TINYINT,
            year SMALLINT,
            yearmo INT,
            fiscal_month TINYINT,
            fiscal_quarter TINYINT,
            fiscal_year SMALLINT,
            last_day_in_month_flag CHAR(1),
            same_day_year_ago_date SMALLDATETIME,
            PRIMARY KEY (date_key)
        )
        """
    )

    # Define the date range from "May 30, 2020" to "September 26, 2023"
    start_date = datetime.date(2020, 5, 30)
    end_date = datetime.date(2023, 9, 26)
    current_date = start_date
    date_key = 0

    # Insert values into the date_dimension table for the specified date range
    while current_date <= end_date:
        date_key += 1
        full_date = current_date.strftime("%Y-%m-%d")
        day_of_week = current_date.weekday() + 1
        day_num_in_month = current_date.day
        day_num_overall = (current_date - start_date).days + 1
        day_name = current_date.strftime("%A")
        day_abbrev = current_date.strftime("%a")
        weekday_flag = "Weekend" if day_of_week in (6, 7) else "Weekday"
        week_num_in_year = current_date.strftime("%U")
        week_num_overall = (current_date - start_date).days // 7 + 1
        week_begin_date = current_date - datetime.timedelta(days=current_date.weekday())
        week_begin_date_key = (week_begin_date - start_date).days + 1
        month = current_date.month
        month_num_overall = (
            current_date.year - start_date.year
        ) * 12 + current_date.month
        month_name = current_date.strftime("%B")
        month_abbrev = current_date.strftime("%b")
        quarter = (current_date.month - 1) // 3 + 1
        year = current_date.year
        yearmo = int(current_date.strftime("%Y%m"))
        fiscal_month = (current_date.month + 6) % 12 or 12
        fiscal_quarter = (fiscal_month - 1) // 3 + 1
        fiscal_year = year if fiscal_month <= 6 else year + 1
        last_day_in_month_flag = (
            "Month End"
            if current_date.month != (current_date + datetime.timedelta(days=1)).month
            else "Not Month End"
        )
        same_day_year_ago_date = current_date - datetime.timedelta(days=365)

        cursor.execute(
            """
            INSERT INTO date_dimension VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date_key,
                full_date,
                day_of_week,
                day_num_in_month,
                day_num_overall,
                day_name,
                day_abbrev,
                weekday_flag,
                week_num_in_year,
                week_num_overall,
                week_begin_date,
                week_begin_date_key,
                month,
                month_num_overall,
                month_name,
                month_abbrev,
                quarter,
                year,
                yearmo,
                fiscal_month,
                fiscal_quarter,
                fiscal_year,
                last_day_in_month_flag,
                same_day_year_ago_date,
            ),
        )

        # Move to the next date
        current_date += datetime.timedelta(days=1)

    # Commit the changes to the database
    conn.commit()
    print("date_dimension table created and populated successfully!")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

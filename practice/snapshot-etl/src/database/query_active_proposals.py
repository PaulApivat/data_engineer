import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = "lido_space.db"
conn = sqlite3.connect(db_path)

# Define the SQL query to join and filter the tables
query = """
    SELECT
        lp.id AS proposal_id,
        lp.title,
        lp.start,
        lp.end,
        lv.voter,
        lv.space_id
    FROM
        lido_proposals AS lp
    INNER JOIN
        lido_votes AS lv
    ON
        lp.id = lv.proposal_id
    WHERE
        lp.state = 'active'
"""

# Execute the query and fetch the result into a DataFrame
result_df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Print the resulting DataFrame
print(result_df)

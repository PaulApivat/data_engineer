import sqlite3

# Define the path to the SQLite database
db_path = "lido_space.db"

# Create a SQLite database connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define the SQL command to create the 'lido_proposals' table with appropriate data types
create_table_sql = """
CREATE TABLE IF NOT EXISTS lido_proposals (
    id TEXT PRIMARY KEY,
    ipfs TEXT,
    title TEXT,
    body TEXT,
    start DATETIME,
    end DATETIME,
    state TEXT,
    author TEXT,
    created DATETIME,
    choices BLOB,
    scores BLOB,
    space TEXT,
    scores_state TEXT,
    scores_total REAL,
    votes INTEGER,
    quorum INTEGER,
    symbol TEXT,
    flagged BOOLEAN
);
"""

# Execute the SQL command to create the table
cursor.execute(create_table_sql)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("lido_proposals table created successfully.")

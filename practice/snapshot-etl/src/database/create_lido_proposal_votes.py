import sqlite3

# Define the path to the SQLite database
db_path = "lido_proposal_votes.db"

# Create a SQLite database connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define the SQL command to create the 'lido_proposals' table with appropriate data types
create_proposals_table_sql = """
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
    space TEXT,
    scores_state TEXT,
    scores_total REAL,
    votes_count INTEGER,
    quorum INTEGER,
    symbol TEXT,
    flagged BOOLEAN
);
"""

# Define the SQL command to create the 'lido_votes' table with appropriate data types
create_votes_table_sql = """
CREATE TABLE IF NOT EXISTS lido_votes (
    id TEXT PRIMARY KEY,
    proposal_id TEXT,
    voter TEXT,
    created DATETIME,
    choice TEXT,
    space TEXT,
    FOREIGN KEY (proposal_id) REFERENCES lido_proposals (id)
);
"""

# Execute the SQL commands to create the tables
cursor.execute(create_proposals_table_sql)
cursor.execute(create_votes_table_sql)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("SQLite tables created successfully.")

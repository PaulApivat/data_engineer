import sqlite3

# Define the path to the SQLite database
db_path = "rocketpool_space.db"

# Create a SQLite database connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# Define the SQL command to create the 'lido_votes' table with appropriate data types
create_votes_table_sql = """
CREATE TABLE IF NOT EXISTS rocketpool_votes (
    id TEXT PRIMARY KEY,
    voter TEXT,
    created DATETIME,
    choice INTEGER,
    space_id TEXT,
    proposal_id TEXT,
    FOREIGN KEY (proposal_id) REFERENCES rocketpool_proposals (id)
);
"""

# Execute the SQL commands to create the tables
cursor.execute(create_votes_table_sql)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("SQLite table: RocketPool_votes created successfully.")

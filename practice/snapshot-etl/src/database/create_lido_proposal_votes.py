import sqlite3

# Define the path to the SQLite database
db_path = "lido_space.db"

# Create a SQLite database connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# Define the SQL command to create the 'lido_votes' table with appropriate data types
create_votes_table_sql = """
CREATE TABLE IF NOT EXISTS lido_votes (
    id TEXT PRIMARY KEY,
    voter TEXT,
    created DATETIME,
    choice INTEGER,
    space_id TEXT,
    proposal_id TEXT,
    FOREIGN KEY (proposal_id) REFERENCES lido_proposals (id)
);
"""

# Execute the SQL commands to create the tables
cursor.execute(create_votes_table_sql)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("SQLite table: lido_votes created successfully.")

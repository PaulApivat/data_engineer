import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("lido_space.db")
cursor = conn.cursor()

# Add an "embedding_id" column to the "lido_proposals" table
cursor.execute("ALTER TABLE lido_proposals ADD COLUMN embedding_id INTEGER")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Added 'embedding_id' column to 'lido_proposals' table.")

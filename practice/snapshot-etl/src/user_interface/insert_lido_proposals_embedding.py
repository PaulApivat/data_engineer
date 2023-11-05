import sqlite3
import pickle

# Load the embeddings dictionary from the pickle file
with open("embeddings.pickle", "rb") as f:
    embeddings_kv_store = pickle.load(f)

# Database connection
db_path = "lido_space.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the "lido_embeddings" table if it doesn't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS lido_embeddings (
        proposal_id TEXT,
        embedding_id INTEGER,
        embedding BLOB,
        PRIMARY KEY (proposal_id, embedding_id),
        FOREIGN KEY (proposal_id) REFERENCES lido_proposals (id)
    )
    """
)

# Insert data from the embeddings dictionary into the "lido_embeddings" table
for (proposal_id, embedding_id), embedding in embeddings_kv_store.items():
    # Convert the embedding to bytes using pickle serialization
    embedding_bytes = pickle.dumps(embedding)

    cursor.execute(
        "INSERT INTO lido_embeddings (proposal_id, embedding_id, embedding) VALUES (?, ?, ?)",
        (proposal_id, embedding_id, sqlite3.Binary(embedding_bytes)),
    )

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("Embeddings stored in the 'lido_embeddings' table successfully.")

import sqlite3
import pickle

# Database connection
db_path = "lido_space.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to retrieve the first row of the "lido_embeddings" table
cursor.execute("SELECT embedding FROM lido_embeddings LIMIT 1")

# Fetch the result
result = cursor.fetchone()

if result is not None:
    # Extract the BLOB data
    embedding_blob = result[0]

    # Deserialize the BLOB data using pickle
    embedding = pickle.loads(embedding_blob)

    # Now, 'embedding' contains the deserialized data that you can work with
    print("Deserialized Embedding:")
    print(embedding)
else:
    print("No data found in the 'lido_embeddings' table.")

# Close the database connection
conn.close()

import sqlite3
import json
import openai
import os
from tiktoken import get_encoding
from openai.embeddings_utils import get_embedding
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("openai.api_key")

# Initialize the dictionary for embeddings
embeddings_kv_store = {}

# Initialize a list to store updated proposals
proposals_with_embeddings_keys = []

# Database connection
db_path = "lido_space.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get the encoding method
# Embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # Encoding for text-embedding-ada-002
max_tokens = 8000  # Maximum for text-embedding-ada-002 is 8191

encoding = get_encoding(embedding_encoding)

# Query proposals from the 'lido_proposals' table
query = "SELECT id, title, body FROM lido_proposals"
cursor.execute(query)
proposals = cursor.fetchall()


# Define a function to store embeddings and update proposals
def store_embeddings_and_update_proposals(proposal_id, combined_text):
    # Count the number of tokens using the specific encoding
    n_tokens = len(encoding.encode(combined_text))

    # Check if the text is within the token limit
    if n_tokens <= max_tokens:
        # Generate the embedding
        embedding = get_embedding(combined_text, engine=embedding_model)

        # Determine the embedding_id (you can use any suitable logic)
        embedding_id = len(embeddings_kv_store) + 1

        # Store the embedding in the dictionary
        embeddings_kv_store[(proposal_id, embedding_id)] = embedding

        return embedding_id
    else:
        return None


# Loop through each proposal
for proposal in proposals:
    proposal_id, title, body = proposal

    # Combine title and body
    combined_text = f"title: {title}, content: {body}"

    # Store the embedding and get the embedding_id
    embedding_id = store_embeddings_and_update_proposals(proposal_id, combined_text)

    if embedding_id is not None:
        # Add the embedding_id to the proposal
        cursor.execute(
            "UPDATE lido_proposals SET embedding_id = ? WHERE id = ?",
            (embedding_id, proposal_id),
        )

        # Commit the changes to the database
        conn.commit()

# Close the database connection
conn.close()

# Write the embeddings dictionary to a pickle file
import pickle

with open("embeddings.pickle", "wb") as f:
    pickle.dump(embeddings_kv_store, f)

print("Embeddings stored and proposals updated successfully.")

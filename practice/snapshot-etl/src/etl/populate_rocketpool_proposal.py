import requests
import pandas as pd
import sqlite3
import json

# Define the SQLite database path
db_path = "rocketpool_space.db"

# Initialize variables
url = "https://hub.snapshot.org/graphql"
first = 6
space_in = ["rocketpool-dao.eth"]
state = "all"
skip = 0

# Create a SQLite database connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define the SQL command to insert data into the 'lido_proposals' table
insert_data_sql = """
INSERT OR REPLACE INTO rocketpool_proposals (
    id, ipfs, title, body, start, end, state, author, created, choices, scores, space, 
    scores_state, scores_total, votes, quorum, symbol, flagged
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Infinite loop for pagination
while True:
    # GraphQL query parameters
    payload = {
        "operationName": "Proposals",
        "variables": {
            "first": first,
            "skip": skip,
            "space_in": space_in,
            "state": state,
            "author_in": [],
            "title_contains": "",
            "flagged": False,
        },
        "query": """query Proposals($first: Int!, $skip: Int!, $state: String!, $space: String, $space_in: [String], $author_in: [String], $title_contains: String, $space_verified: Boolean, $flagged: Boolean) {
                      proposals(
                        first: $first,
                        skip: $skip,
                        where: {space: $space, state: $state, space_in: $space_in, author_in: $author_in, title_contains: $title_contains, space_verified: $space_verified, flagged: $flagged}
                      ) {
                        id
                        ipfs
                        title
                        body
                        start
                        end
                        state
                        author
                        created
                        choices
                        space {
                          id
                          name
                          members
                          avatar
                          symbol
                          verified
                          plugins
                        }
                        scores_state
                        scores_total
                        scores
                        votes
                        quorum
                        symbol
                        flagged
                      }
                    }""",
    }

    # Make the request
    response = requests.post(url, json=payload)
    data = response.json()

    # Extract proposals
    proposals = data.get("data", {}).get("proposals", [])

    # Break loop if no more proposals
    if not proposals:
        break

    # Transform the data into a DataFrame
    df = pd.DataFrame(proposals)

    # Iterate through DataFrame and insert data into SQLite table
    for _, row in df.iterrows():
        # Convert the 'choices' column to a JSON string
        choices_json = json.dumps(row["choices"])
        scores_json = json.dumps(row["scores"])

        proposal_data = (
            row["id"],
            row["ipfs"],
            row["title"],
            row["body"],
            row["start"],
            row["end"],
            row["state"],
            row["author"],
            row["created"],
            choices_json,  # Insert the JSON string
            # row["choices"],
            scores_json,  # Insert the JSON string for 'scores'
            # row["scores"],
            row["space"]["name"],
            row["scores_state"],
            row["scores_total"],
            row["votes"],
            row["quorum"],
            row["symbol"],
            row["flagged"],
        )
        cursor.execute(insert_data_sql, proposal_data)

    # Increment skip for pagination
    skip += first

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("---- RocketPool Proposal ETL complete ----")

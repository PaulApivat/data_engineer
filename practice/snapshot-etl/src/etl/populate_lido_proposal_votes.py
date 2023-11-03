import requests
import pandas as pd
import json
import sqlite3

# Initialize variables
url = "https://hub.snapshot.org/graphql"
first = 6
space_in = ["lido-snapshot.eth"]
state = "all"
db_path = "lido_space.db"  # SQLite database path


# Function to fetch proposals
def fetch_proposals(skip):
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

    return proposals


# Function to fetch and insert votes for a proposal into SQLite
def fetch_and_insert_votes(cursor, proposal_id):
    payload = {
        "operationName": "Votes",
        "variables": {"proposal": proposal_id},
        "query": """query Votes($proposal: String!) {
                      votes(
                        first: 1000,
                        where: {proposal: $proposal}
                      ) {
                        id
                        voter
                        created
                        choice
                        space {
                          id
                        }
                      }
                    }""",
    }

    # Make the request
    response = requests.post(url, json=payload)
    data = response.json()

    # Extract and insert votes
    votes = data.get("data", {}).get("votes", [])
    for vote in votes:
        # Check if 'choice' is an integer
        if isinstance(vote["choice"], int):
            # Handle the integer value as needed
            choice = vote["choice"]
        elif "choice" in vote and str(vote["choice"]).isdigit():
            # Convert 'choice' to an integer if it's a string containing digits
            choice = int(vote["choice"])
        else:
            # Handle other cases, e.g., set it to None
            choice = None

        # Insert vote data into 'lido_votes' table
        cursor.execute(
            """
            INSERT OR REPLACE INTO lido_votes (id, voter, created, choice, space_id, proposal_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                vote["id"],
                vote["voter"],
                vote["created"],
                choice,  # Insert the integer value or None based on the handling
                vote["space"]["id"] if "space" in vote else None,
                proposal_id,
            ),
        )


# Create a SQLite database connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Main loop to fetch and process proposals and their votes
skip = 0
while True:
    proposals = fetch_proposals(skip)

    # Break loop if no more proposals
    if not proposals:
        break

    # Process each proposal and fetch/insert votes
    for proposal in proposals:
        proposal_id = proposal["id"]
        fetch_and_insert_votes(cursor, proposal_id)

    # Increment skip for pagination
    skip += first

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("----Lido ETL complete ----")
print("Data inserted into lido_votes table successfully.")

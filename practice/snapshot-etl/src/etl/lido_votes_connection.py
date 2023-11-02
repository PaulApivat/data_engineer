import requests
import pandas as pd

# Initialize variables
url = "https://hub.snapshot.org/graphql"
first = 6
space_in = ["lido-snapshot.eth"]
state = "all"


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


# Function to fetch and print votes for each proposal
def fetch_and_print_votes(proposal_id):
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

    # Extract and print votes
    votes = data.get("data", {}).get("votes", [])
    df = pd.DataFrame(votes)
    print("Votes for Proposal ID:", proposal_id)
    print(df)
    print("\n")
    print(df.dtypes)


# Main loop to fetch and process proposals
skip = 0
while True:
    proposals = fetch_proposals(skip)

    # Break loop if no more proposals
    if not proposals:
        break

    # Process each proposal and fetch votes
    for proposal in proposals:
        proposal_id = proposal["id"]
        fetch_and_print_votes(proposal_id)

    # Increment skip for pagination
    skip += first

print("----Lido ETL complete ----")

print("----Lido Votes nested in Proposals ETL complete ----")

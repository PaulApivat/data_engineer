import requests
import pandas as pd

# Initialize variables
url = "https://hub.snapshot.org/graphql"
skip = 0
first = 6
space_in = ["lido-snapshot.eth"]
state = "all"

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

    # Print the DataFrame
    print(df)

    # Increment skip for pagination
    skip += first

print("----Lido ETL complete ----")

import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = "lido_space.db"  # Replace with the actual path to your database
conn = sqlite3.connect(db_path)

# Step 1: Check if proposal.id exists in 'lido_votes'
query_step1 = """
    SELECT DISTINCT lp.id AS proposal_id
    FROM lido_proposals AS lp
    WHERE NOT EXISTS (
        SELECT 1
        FROM lido_votes AS lv
        WHERE lp.id = lv.proposal_id
    )
"""

step1_result_df = pd.read_sql_query(query_step1, conn)

# Step 2: Check if 'id' exists in 'lido_proposals'
query_step2 = """
    SELECT DISTINCT proposal_id
    FROM lido_votes
    WHERE NOT EXISTS (
        SELECT 1
        FROM lido_proposals
        WHERE proposal_id = id
    )
"""

step2_result_df = pd.read_sql_query(query_step2, conn)

# Step 3: Print out all active proposals and relevant data
query_active_proposals = """
    SELECT lp.id AS proposal_id, lp.title, lp.start, lp.end, lv.voter, lv.choice
    FROM lido_proposals AS lp
    INNER JOIN lido_votes AS lv ON lp.id = lv.proposal_id
    WHERE lp.state = "active"
"""

active_proposals_df = pd.read_sql_query(query_active_proposals, conn)


# Close the database connection
conn.close()

# Print the results
print("Step 1 - Proposals without votes:")
print(step1_result_df)

print("\nStep 2 - Votes without matching proposals:")
print(step2_result_df)

print("\nActive Proposals:")
print(active_proposals_df)

import sqlite3

# Define the path to your SQLite database
db_path = "rocketpool.db"

# Specify the id of the row to be deleted
row_id_to_delete = 4791  # Replace with the actual id

# Create a connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # SQL query to delete a specific row
    cursor.execute(
        "DELETE FROM protocol_topics_post_pages WHERE id = ?", (row_id_to_delete,)
    )

    # Commit the changes to the database
    conn.commit()
    if cursor.rowcount > 0:
        print(
            f"Row with id {row_id_to_delete} deleted successfully from protocol_topics_post_pages!"
        )
    else:
        print(f"No row found with id {row_id_to_delete} in protocol_topics_post_pages.")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()

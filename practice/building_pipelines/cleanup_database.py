import sqlite3

def delete_tables(db_name, table_names):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)

    # Create a cursor object
    cursor = conn.cursor()

    for table in table_names:
        # Formulate the SQL command
        drop_table_command = f"DROP TABLE IF EXISTS {table}"

        # Execute the command
        cursor.execute(drop_table_command)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == "__main__":
    # Name of the SQLite database
    db_name = "practice_database.db"

    # List of table names to be deleted
    table_names = ["people", "cryptoscam", "market_dom", "news", "price_change", 
                   "rsi", "market_cap", "price_change_2", "volume", "volume_2", "rsi_2", "market_cap_2",
                   "market_dom_2", "news_2", "contracts", "active_address", "txnfee", "eth_price",
                   "burn", "emissions", "txnfee_df", "burn_df", "emissions_df"]

    delete_tables(db_name, table_names)
    print(f"Tables {table_names} have been successfully deleted from {db_name}.")

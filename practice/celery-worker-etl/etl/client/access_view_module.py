import sqlite3
import pandas as pd

class EthFeesView:
    def __init__(self, db_path):
        self.db_path = db_path
        self.view_name = "eth_fees_chart_view"

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_data(self):
        try:
            # Connect to the SQLite database
            conn = self._connect()

            # Define a query to retrieve data from the view
            query = f"SELECT * FROM {self.view_name}"

            # Execute the query and convert the result into a DataFrame
            df = pd.read_sql_query(query, conn)

            return df

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the database connection
            conn.close()

if __name__ == "__main__":
    # Example usage:
    db_path = "raw_bronze.db"
    eth_fees = EthFeesView(db_path)
    df = eth_fees.get_data()

    # Print the DataFrame or perform further processing
    print(df)
import unittest
import duckdb
import json
import jsonschema


class TestEthEmissionsValidation(unittest.TestCase):
    def test_validation(self):
        # Define the path to the schema file
        schema_path = "config/schema_definitions/eth_emissions_silver_schema.json"

        # Read the JSON schema from the file
        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)

        # Connect to the DuckDB database
        db_path = "data/silver/transform_data.db"
        conn = duckdb.connect(db_path)

        # Define the table name
        table_name = "eth_emissions_silver"

        # Fetch data from the table
        query = f"SELECT * FROM {table_name}"
        df = conn.execute(query).fetchdf()

        # Convert DataFrame to a list of dictionaries (one per row)
        data = df.to_dict(orient="records")

        # Convert the 'datetime' column to string format
        for row in data:
            row["datetime"] = str(row["datetime"])  # Convert Timestamp to string

        # Validate each row against the JSON schema
        for row in data:
            try:
                jsonschema.validate(instance=row, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                self.fail(f"Validation error for row: {row}\nError message: {e}")

        # Close the database connection
        conn.close()


if __name__ == "__main__":
    unittest.main()

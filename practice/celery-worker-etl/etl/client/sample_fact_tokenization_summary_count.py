import os
import logging
from dotenv import load_dotenv
from dotenv import load_dotenv
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase


load_dotenv()
api_key = os.getenv("DUNE_API_KEY_TEAM")

logger = logging.getLogger()
logger.level = logging.DEBUG


def main():
    # Define the query with parameters
    query = QueryBase(
        name="sample_fact_tokenization_summary_count",
        query_id=3113672,
    )

    print("Results available at", query.url())

    # Create a DuneClient and run the query
    dune = DuneClient.from_env()
    results = dune.run_query(query)
    logger.info(results)

    # Access data directly from the ResultsResponse object
    if results.result:
        metadata = results.result.metadata
        print("Metadata:", metadata)
        print("Result Set Bytes:", metadata.result_set_bytes)
        print("Total Row Count:", metadata.total_row_count)
        print("Data Point Count:", metadata.datapoint_count)
    else:
        print("Results not found in the response.")


if __name__ == "__main__":
    main()

## UI - test run, Medium Cluster, 11 mins, no parameters.

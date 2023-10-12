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
        name="Sample Query",
        query_id=3091918,
        params=[
            QueryParameter.date_type(name="1. start_date", value="2023-04-01 00:00:00"),
            QueryParameter.date_type(name="2. end_date", value="2023-10-01 00:00:00"),
            QueryParameter.number_type(name="offset", value=10),
            QueryParameter.number_type(name="limit", value=10),
        ],
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

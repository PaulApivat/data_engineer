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
        name=" t3_eth_fees_weekly_count",
        query_id=3095734,
        params=[
            QueryParameter.date_type(name="1. start_date", value="2023-04-01 00:00:00"),
            QueryParameter.date_type(name="2. end_date", value="2023-10-01 00:00:00"),
        ],
    )

    print("Results available at", query.url())

    # Create a DuneClient and run the query
    dune = DuneClient.from_env()
    results = dune.run_query(query)
    logger.info(results)


if __name__ == "__main__":
    main()

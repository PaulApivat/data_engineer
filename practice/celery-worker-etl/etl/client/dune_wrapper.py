import logging
import sys
import unittest
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DUNE_API_KEY_TEAM")

from dune_client.client import DuneClient
from dune_client.query import QueryBase

logger = logging.getLogger()
logger.level = logging.DEBUG


class TestDuneAPI(unittest.TestCase):
    def test_wrapper_query(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)
        query = QueryBase(
            name="samaple t3_eth_fees_weekly_params", query_id=3091918
        )  # eth_emissions: 3032256 #eth_emissions_params: 3088161
        dune = DuneClient.from_env()
        results = dune.run_query(query)
        logger.info(results)


if __name__ == "__main__":
    unittest.main()

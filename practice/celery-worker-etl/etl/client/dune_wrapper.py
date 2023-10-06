import logging
import sys
import unittest
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DUNE_API_KEY")

from dune_client.client import DuneClient
from dune_client.query import QueryBase

logger = logging.getLogger()
logger.level = logging.DEBUG


class TestDuneAPI(unittest.TestCase):
    def test_wrapper_query(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)
        query = QueryBase(name="samaple eth_emissions", query_id=3032256)
        dune = DuneClient.from_env()
        results = dune.run_query(query)
        logger.info(results)


if __name__ == "__main__":
    unittest.main()

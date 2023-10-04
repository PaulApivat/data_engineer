from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch your API key from the environment variables
api_key = os.getenv("DUNE_API_KEY")

query = QueryBase(
    name="Sample Query",
    query_id=1215383,
    params=[
        QueryParameter.text_type(name="TextField", value="Word"),
        QueryParameter.number_type(name="NumberField", value=3.1415926535),
        QueryParameter.date_type(name="DateField", value="2022-05-04 00:00:00"),
        QueryParameter.enum_type(name="ListField", value="Option 1"),
    ],
)
print("Results available at", query.url())

dune = DuneClient.from_env()
try:
    results = dune.run_query(query)
except Exception as e:
    print(f"Error executing query: {e}")


# SELECT
#     days as datetime,
#     TRY_CAST(net_emission_eth AS REAL) as net_emission_eth,
#     TRY_CAST(SUM(net_emission_eth) OVER (ORDER BY days ASC ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as REAL) as total_net_emission_eth
# FROM (
#     SELECT
#         s.days
#         , TRY_CAST(s.total_reward - coalesce(s.total_base_eth, 0) AS DECIMAL(20,4)) as net_emission_eth
#     FROM (
#         SELECT
#             DATE_TRUNC('day', t.block_time) AS days
#             , COUNT(DISTINCT b."number") * 2 AS total_reward
#             , SUM(CASE WHEN t.block_number >= 12965000 THEN (b.base_fee_per_gas / pow(10,9)) * (t.gas_used / pow(10,9)) ELSE NULL END) AS total_base_eth
#         FROM ethereum.transactions t
#         INNER JOIN ethereum.blocks b ON b."number" = t.block_number AND b.time = t.block_time
#         WHERE DATE_TRUNC('day', t.block_time) < CURRENT_DATE
#         AND success
#         GROUP BY 1
#     ) s
# ) AS sub
# ORDER BY days DESC limit {{limit}}

import os
import logging
from dotenv import load_dotenv
from dune_client.types import QueryParameter
from dune_client.query import QueryBase
from dune_client.api.execution import ExecutionAPI, BaseRouter
from dune_client.models import ExecutionResponse
import time

load_dotenv()
api_key = os.getenv("DUNE_API_KEY_TEAM")

# Configure logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger()


class CustomExecutionAPI(ExecutionAPI):
    def __init__(self, base_router: BaseRouter):
        super().__init__(
            base_router.token,
            base_router.base_url,
            base_router.request_timeout,
            base_router.client_version,
            base_router.performance,
        )

    def execute_query(self, query: QueryBase) -> ExecutionResponse:
        return super().execute_query(query)


def main():
    # Define the query with parameters
    query = QueryBase(
        name="sample_fact_tokenization_summary_mv_execapi",
        query_id=3125259,
        params=[
            QueryParameter.number_type(name="offset", value=1000),
            QueryParameter.number_type(name="limit", value=10000),
        ],
    )

    print("Results available at", query.url())

    # Create an instance of the BaseRouter class with your API key
    dune = BaseRouter(api_key=api_key)

    # Create an instance of the CustomExecutionAPI class using the BaseRouter instance
    execution_api = CustomExecutionAPI(dune)

    # Execute the query
    execution_response = execution_api.execute_query(query)

    if execution_response.state == "QUERY_STATE_COMPLETE":
        job_id = execution_response.job_id
        print("Execution successful. Job ID:", job_id)

        # Use the ExecutionAPI to get execution status and results
        execution_status = execution_api.get_execution_status(job_id)
        execution_results = execution_api.get_execution_results(job_id)

        # Access data from execution_status and execution_results as needed
        print("Execution Status:", execution_status)
        print("Execution Results:", execution_results)
    elif execution_response.state == "QUERY_STATE_PENDING":
        # Execution is pending, wait and check again until it's complete
        max_retries = 10  # Set the maximum number of retries
        retries = 0

        while (
            execution_response.state == "QUERY_STATE_PENDING" and retries < max_retries
        ):
            time.sleep(60)  # Wait for 60 seconds (adjust this as needed)
            execution_response = execution_api.get_execution_status(
                execution_response.job_id
            )
            retries += 1

        if execution_response.state == "QUERY_STATE_COMPLETE":
            job_id = execution_response.job_id
            print("Execution successful. Job ID:", job_id)

            # Use the ExecutionAPI to get execution status and results
            execution_status = execution_api.get_execution_status(job_id)
            execution_results = execution_api.get_execution_results(job_id)

            # Access data from execution_status and execution_results as needed
            print("Execution Status:", execution_status)
            print("Execution Results:", execution_results)
        else:
            print("Execution failed after retries.")
    else:
        print("Execution failed.")


if __name__ == "__main__":
    main()

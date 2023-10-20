import os
import logging
import requests
import time
from dotenv import load_dotenv
from dune_client.api.execution import ExecutionAPI, BaseRouter
from dune_client.models import ExecutionStatusResponse, ResultsResponse, ExecutionState

load_dotenv()
api_key = os.getenv("DUNE_API_KEY_TEAM")

logger = logging.getLogger()
logger.level = logging.DEBUG


def get_execution_id(query_id: int, api_key: str) -> str:
    # Define the base URL and headers
    base_url = f"https://api.dune.com/api/v1/query/{query_id}/execute"
    headers = {"X-Dune-API-Key": api_key}

    # Define query parameters, in this case, "performance" as "medium"
    params = {
        "performance": "medium",
    }

    # Send a POST request to execute the query
    result_response = requests.post(base_url, headers=headers, params=params)

    # Check if the request was successful
    if result_response.status_code == 200:
        # Extract the execution ID (job_id) from the response
        response_json = result_response.json()
        execution_id = response_json.get("execution_id")
        return execution_id
    else:
        # Handle the case where the query execution failed
        print("Query execution failed with status code:", result_response.status_code)
        return None


def main():
    # Replace with the actual query ID you want to execute
    query_id_to_execute = 3125259

    # Access the API key as a string
    api_key = os.getenv("DUNE_API_KEY_TEAM")

    # Get the execution ID (job_id) by executing the query
    execution_id = get_execution_id(query_id_to_execute, api_key)

    if execution_id:
        print(f"Execution ID (job_id): {execution_id}")

        # Create an instance of the ExecutionAPI class with your API key
        execution_api = ExecutionAPI(api_key=api_key)

        # Wait and check the execution status periodically until it reaches a terminal state
        while True:
            execution_status = execution_api.get_execution_status(execution_id)

            if execution_status.state == ExecutionState.COMPLETED:
                print("Execution successful.")
                print("Execution Status:", execution_status)

                # Get the execution results
                execution_results = execution_api.get_execution_results(execution_id)
                print("Execution Results:", execution_results)
                break  # Query execution is complete, exit the loop

            elif execution_status.state == ExecutionState.FAILED:
                print("Execution failed.")
                print("Execution Status:", execution_status)
                break

            elif execution_status.state == ExecutionState.CANCELLED:
                print("Execution cancelled by user.")
                print("Execution Status:", execution_status)
                break

            elif execution_status.state == ExecutionState.PENDING:
                print("Execution is still pending. Waiting...")
                # Wait for a few seconds before checking again (adjust as needed)
                time.sleep(10)


if __name__ == "__main__":
    main()

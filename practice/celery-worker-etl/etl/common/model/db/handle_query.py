from sqlalchemy.orm import sessionmaker
from dune_client.client import DuneClient
from dune_client.query import QueryBase

# Assuming you have your engine and Base already set up from your initialization script
from .database_init import engine
from . import Base
from .raw_model import RecordedRawMetric
from .etl_reference_master_model import DigitalAssetMetric
from datetime import datetime


# environment
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("DUNE_API_KEY")
Session = sessionmaker(bind=engine)
session = Session()


def handle_query(metric, your_start_date, your_end_date):
    # initiation session at start of function

    # 2. Run the external API call
    dune = DuneClient(api_key)

    query = QueryBase(name="eth_emissions_params", query_id=3088161)

    results = dune.run_query(query)
    print(results)

    # Check if the results contain a 'result' attribute
    if results.result:
        print(f"Saving results for query associated with metric UUID: {metric.uuid}")
        result_rows = results.result.rows

        # 3. Process the results
        insert_or_update_values = []
        for row in result_rows:
            db_metric = RecordedRawMetric(
                # Unique UUID is auto-generated, no need to set metric_uuid here
                datetime=datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S.%f %Z"),
                net_emission_eth=row["net_emission_eth"],  # Adjusted column name
                total_net_emission_eth=row[
                    "total_net_emission_eth"
                ],  # Added new column data
            )
            insert_or_update_values.append(db_metric)

        # 4. Upsert the records into the database
        session.bulk_save_objects(insert_or_update_values)
        session.commit()

    # 5. Close the database session
    session.close()


# Before calling handle_query, retrieve your_metric:
target_datetime = datetime.strptime(
    "2023-10-06T12:00:00.000 UTC", "%Y-%m-%dT%H:%M:%S.%f %Z"
)
your_metric = (
    session.query(DigitalAssetMetric).filter_by(datetime=target_datetime).first()
)

# Check if the metric was retrieved successfully
if not your_metric:
    raise ValueError("No DigitalAssetMetric found for specified datetime")

# Define your start and end dates:
your_start_date = "2023-09-01"  # adjust as needed
your_end_date = "2023-10-01"  # adjust as needed

# To run the function:
handle_query(your_metric, your_start_date, your_end_date)

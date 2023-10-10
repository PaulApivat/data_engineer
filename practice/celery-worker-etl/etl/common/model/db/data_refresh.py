import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from .handle_query import handle_query
from .etl_reference_master_model import DigitalAssetMetric
from .raw_model import RecordedRawMetric
from .database_init import engine

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def refresh_data():
    # 1. Initiate a database session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # This will represent the date until which you want to fetch data (yesterday)
        your_end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        # To determine the start date, you'll check the last date available in your RecordedRawMetric
        last_metric_date = (
            session.query(RecordedRawMetric.datetime)
            .order_by(RecordedRawMetric.datetime.desc())
            .first()
        )
        if last_metric_date:
            your_start_date = (last_metric_date[0] + timedelta(days=1)).strftime(
                "%Y-%m-%d"
            )
        else:
            # If there's no data, set a default start date
            your_start_date = "2023-10-07"

        # Logging the determined start and end dates
        logger.info(f"Fetching data from {your_start_date} to {your_end_date}.")

        # Check if any metric exists in the database (assuming that's relevant for your logic)
        your_metric = session.query(DigitalAssetMetric).first()

        # If there's no metric, log an error and raise an exception
        if not your_metric:
            logger.error("No DigitalAssetMetric found in the database.")
            raise ValueError("No DigitalAssetMetric found in the database.")

        # Run the function:
        handle_query(your_metric, your_start_date, your_end_date)

        session.commit()  # Commit at the end if everything succeeds

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        session.rollback()

    finally:
        # Close the database session
        session.close()


# If you want to run this script directly
if __name__ == "__main__":
    refresh_data()

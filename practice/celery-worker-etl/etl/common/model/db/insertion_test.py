from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .etl_reference_master_model import DigitalAssetMetric
from .raw_model import RecordedRawMetric  # Import the model
import sys
from . import Base

sys.path.append(
    "/Users/paulapivat/Desktop/local_github/data_engineer/practice/celery-worker-etl"
)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to bronze.db relative to the script
db_path = os.path.join(script_dir, "bronze.db")

# Setup database connection
DATABASE_URL = f"sqlite:///{db_path}"  # Adjusted to point to the correct bronze.db
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(engine)  # This will create all tables related to the models

# Create a new session
session = SessionLocal()

# Insert a sample metric for DigitalAssetMetric
sample_metric = DigitalAssetMetric(
    datetime_str="2023-10-06T12:00:00.000 UTC",
    net_emission_eth=10814,
    total_net_emission_eth=1008096,
)
session.add(sample_metric)
session.commit()
session.close()

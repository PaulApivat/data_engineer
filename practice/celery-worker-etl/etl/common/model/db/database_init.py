import datetime
import uuid
from sqlalchemy import create_engine, Column, String, DateTime, Integer
from . import Base
from .etl_reference_master_model import DigitalAssetMetric
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to bronze.db relative to the script
db_path = os.path.join(script_dir, "bronze.db")

DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True to log SQL activities

if __name__ == "__main__":
    print(Base.metadata.tables)
    Base.metadata.create_all(engine)

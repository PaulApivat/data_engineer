import uuid
import logging

from sqlalchemy import Column, ForeignKey, Float, DateTime, String
from sqlalchemy.orm import relationship
from . import Base, HasCreateTime
from .etl_reference_master_model import DigitalAssetMetric

logger = logging.getLogger("etl.model.db.raw_model")
logger.setLevel(level=logging.INFO)
logging.basicConfig()


class RecordedRawMetric(Base, HasCreateTime):
    __tablename__ = "onchain_recorded_raw_metric"
    metric_uuid = Column(String, ForeignKey(DigitalAssetMetric.uuid), nullable=False)
    record_date = Column(DateTime(timezone=True), nullable=False)
    value = Column(Float, index=False, nullable=False)

    # Adding ORM-style access to DigitalAssetMetric
    digital_asset_metric = relationship("DigitalAssetMetric")

    def __init__(self, metric_uuid, record_date, value):
        super().__init__()
        self.metric_uuid = str(metric_uuid)  # Convert UUID to string for SQLite
        self.record_date = record_date
        self.value = value

    __mapper_args__ = {"primary_key": [metric_uuid, record_date]}


# Ensure DigitalAssetMetric entries are inserted before RecordedRawMetric entries.
# Otherwise, there may be integrity errors.

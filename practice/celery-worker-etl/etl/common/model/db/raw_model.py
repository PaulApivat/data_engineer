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
    # Generate a unique UUID for each row
    metric_uuid = Column(
        String,
        ForeignKey(DigitalAssetMetric.uuid),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    datetime = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    net_emission_eth = Column(Float, nullable=False)
    total_net_emission_eth = Column(Float, nullable=False)

    # Adding ORM-style access to DigitalAssetMetric
    digital_asset_metric = relationship("DigitalAssetMetric")

    def __init__(self, datetime, net_emission_eth, total_net_emission_eth):
        super().__init__()
        self.datetime = datetime
        self.net_emission_eth = net_emission_eth
        self.total_net_emission_eth = total_net_emission_eth

    __mapper_args__ = {"primary_key": [metric_uuid, datetime]}


# Ensure DigitalAssetMetric entries are inserted before RecordedRawMetric entries.
# Otherwise, there may be integrity errors.

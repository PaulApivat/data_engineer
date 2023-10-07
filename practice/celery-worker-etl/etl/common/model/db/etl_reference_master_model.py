from sqlalchemy import Column, String, DateTime, Integer
from . import Base
import datetime
import uuid


class DigitalAssetMetric(Base):
    __tablename__ = "digital_asset_metric"

    uuid = Column(
        String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False
    )
    datetime = Column(DateTime, nullable=False)
    net_emission_eth = Column(Integer, nullable=False)
    total_net_emission_eth = Column(Integer, nullable=False)

    def __init__(self, datetime_str, net_emission_eth, total_net_emission_eth):
        # datetime string converted to proper datetime object for storage
        self.datetime = datetime.datetime.strptime(
            datetime_str, "%Y-%m-%dT%H:%M:%S.%f %Z"
        )
        self.net_emission_eth = net_emission_eth
        self.total_net_emission_eth = total_net_emission_eth

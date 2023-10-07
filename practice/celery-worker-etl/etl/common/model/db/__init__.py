from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
import datetime

Base = declarative_base()


class HasCreateTime:
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

import requests
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy Model
Base = declarative_base()


class ProtocolUsers(Base):
    __tablename__ = "protocol_users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    trust_level = Column(Integer)
    admin = Column(Boolean)
    moderator = Column(Boolean)


# SQLAlchemy Engine and Session Setup
engine = create_engine("sqlite:///rocketpool.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Fetch Data
url = "https://dao.rocketpool.net/top.json"
# url = "https://dao.rocketpool.net/top.json?period=all"
response = requests.get(url)
if response.status_code == 200:
    json_data = response.json()
    users_data = json_data.get("users", [])
    # extract data
    extracted_data = [
        {
            "id": user.get("id"),
            "username": user.get("username"),
            "name": user.get("name"),
            "trust_level": user.get("trust_level"),
            "admin": user.get("admin"),
            "moderator": user.get("moderator"),
        }
        for user in users_data
    ]
    # convert to dataframe
    df = pd.DataFrame(extracted_data)

    # Insert Data into Database
    data_dicts = df.to_dict(orient="records")
    for data in data_dicts:
        user = ProtocolUsers(**data)
        session.add(user)
    session.commit()
else:
    print("Failed to retrieve data: HTTP Status Code", response.status_code)

# Close Session
session.close()

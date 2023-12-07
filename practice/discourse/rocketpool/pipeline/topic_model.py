from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
import requests
import pandas as pd
import datetime

# SQLAlchemy Model
Base = declarative_base()


class ProtocolTopics(Base):
    __tablename__ = "protocol_topics"
    id = Column(Integer, primary_key=True)
    slug = Column(String)
    title = Column(String)
    created_at = Column(DateTime)
    last_posted_at = Column(DateTime)
    category_id = Column(Integer)
    posters = Column(JSON)  # Storing as JSON
    views = Column(Integer)
    reply_count = Column(Integer)


# Create an engine and tables
engine = create_engine("sqlite:///rocketpool.db")
Base.metadata.create_all(engine)

# Fetch Data
url = "https://dao.rocketpool.net/top.json"
# url = "https://dao.rocketpool.net/top.json?period=all"
response = requests.get(url)
if response.status_code == 200:
    json_data = response.json()

    # Debug: Print out the top-level keys to understand the structure
    # print("Top-level keys:", json_data.keys())

    # Accessing 'topics' inside 'topic_list'
    topic_list = json_data.get("topic_list", {})
    topics_data = topic_list.get("topics", [])
    if not topics_data:
        print("The 'topics' key was not found or is empty.")

    # Process data into a list of dictionaries
    processed_data = []
    for topic in topics_data:
        try:
            processed_data.append(
                {
                    "id": topic.get("id"),
                    "slug": topic.get("slug"),
                    "title": topic.get("title"),
                    "created_at": datetime.datetime.fromisoformat(
                        topic["created_at"].rstrip("Z")
                    )
                    if topic.get("created_at")
                    else None,
                    "last_posted_at": datetime.datetime.fromisoformat(
                        topic["last_posted_at"].rstrip("Z")
                    )
                    if topic.get("last_posted_at")
                    else None,
                    "category_id": topic.get("category_id"),
                    "posters": topic.get("posters"),
                    "views": topic.get("views"),
                    "reply_count": topic.get("reply_count"),
                }
            )
        except Exception as e:
            print(f"Error processing topic {topic.get('id')}: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(processed_data)

    # Insert data into the database
    Session = sessionmaker(bind=engine)
    session = Session()
    for data_dict in df.to_dict(orient="records"):
        topic = ProtocolTopics(**data_dict)
        session.add(topic)
    session.commit()
    session.close()
else:
    print("Failed to retrieve data: HTTP Status Code", response.status_code)

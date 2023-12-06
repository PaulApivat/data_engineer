from sqlalchemy import create_engine, text

# Database engine
engine = create_engine("sqlite:///rocketpool.db")

# Query the database directly with raw SQL
with engine.connect() as connection:
    result = connection.execute(text("SELECT id, slug FROM protocol_topics"))

    # Construct URLs and store them in a list
    # Note: result rows are tuples, so use indices to access elements
    urls = [f"https://dao.rocketpool.net/t/{row[1]}/{row[0]}.json" for row in result]


# Print out the list of URLs
print("List of URLs:")
for url in urls:
    print(url)


from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    Float,
    Boolean,
)
from sqlalchemy.orm import declarative_base, sessionmaker
import requests
import datetime

# SQLAlchemy Model
Base = declarative_base()


class ProtocolTopicsPost(Base):
    __tablename__ = "protocol_topics_post"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    created_at = Column(DateTime)
    cooked = Column(String)
    post_number = Column(Integer)
    reply_to_post_number = Column(Integer, nullable=True)
    updated_at = Column(DateTime)
    incoming_link_count = Column(Integer)
    reads = Column(Integer)
    readers_count = Column(Integer)
    score = Column(Float)
    topic_id = Column(Integer)
    topic_slug = Column(String)
    user_id = Column(Integer)
    user_title = Column(String, nullable=True)
    trust_level = Column(Integer)
    moderator = Column(Boolean, nullable=True)
    admin = Column(Boolean, nullable=True)
    staff = Column(Boolean, nullable=True)
    stream = Column(JSON)  # Storing as JSON


# Define a session
engine = create_engine("sqlite:///rocketpool.db")
# Create the table
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Fetch JSON data for each URL
json_responses = []
for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        json_responses.append(response.json())
    else:
        print(
            f"Failed to retrieve data for URL {url}: HTTP Status Code",
            response.status_code,
        )

# Process each JSON response and insert data into the database
session = Session()
# Insert JSON data into the database

for json_data in json_responses:
    posts_data = json_data.get("post_stream", {}).get("posts", [])
    for post in posts_data:
        try:
            post_entry = ProtocolTopicsPost(
                id=post.get("id"),
                name=post.get("name"),
                username=post.get("username"),
                created_at=datetime.datetime.fromisoformat(
                    post["created_at"].rstrip("Z")
                )
                if post.get("created_at")
                else None,
                cooked=post.get("cooked"),
                post_number=post.get("post_number"),
                reply_to_post_number=post.get("reply_to_post_number"),
                updated_at=datetime.datetime.fromisoformat(
                    post["updated_at"].rstrip("Z")
                )
                if post.get("updated_at")
                else None,
                incoming_link_count=post.get("incoming_link_count"),
                reads=post.get("reads"),
                readers_count=post.get("readers_count"),
                score=post.get("score"),
                topic_id=post.get("topic_id"),
                topic_slug=post.get("topic_slug"),
                user_id=post.get("user_id"),
                user_title=post.get("user_title"),
                trust_level=post.get("trust_level"),
                moderator=post.get("moderator"),
                admin=post.get("admin"),
                staff=post.get("staff"),
                stream=post.get("stream"),
            )
            session.add(post_entry)
        except Exception as e:
            print(f"Error inserting post data: {e}")
session.commit()
session.close()

import requests
import datetime
import logging
import time
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# SQLAlchemy Model
Base = declarative_base()


class ProtocolTopics(Base):
    __tablename__ = "protocol_topics_pages"
    id = Column(Integer, primary_key=True)
    slug = Column(String)
    title = Column(String)
    created_at = Column(DateTime)
    last_posted_at = Column(DateTime)
    category_id = Column(Integer)
    posters = Column(JSON)  # Storing as JSON
    views = Column(Integer)
    reply_count = Column(Integer)
    page = Column(Integer)


class ProtocolUsers(Base):
    __tablename__ = "protocol_users_pages"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    trust_level = Column(Integer)
    admin = Column(Boolean)
    moderator = Column(Boolean)
    page = Column(Integer)


# Create an engine and tables
engine = create_engine("sqlite:///rocketpool.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Function to handle rate limiting
def handle_rate_limiting(delay):
    logging.warning(f"Rate limit reached, sleeping for {delay} seconds")
    time.sleep(delay)


# Function to fetch paginated data
def fetch_paginated_data(url_template, page_start, session):
    page = page_start
    delay = 1  # Start with a 1-second delay for exponential backoff
    while True:
        # paginated_url = url_template.format(page=page)
        paginated_url = f"https://dao.rocketpool.net/top.json?period=all&page={page}"
        logging.info(f"Fetching data from URL: {paginated_url}")
        response = requests.get(paginated_url)

        if response.status_code == 429:  # Rate limit hit
            handle_rate_limiting(delay)
            delay *= 2  # Exponential backoff
            continue

        if response.status_code != 200:
            logging.error(
                f"Failed to fetch data: HTTP status code {response.status_code}"
            )
            break

        json_data = response.json()
        # Check if there are no more topics or users
        if not json_data.get("topic_list", {}).get("topics") and not json_data.get(
            "users"
        ):
            logging.info(f"No more data found at page {page}.")
            break

        delay = 1  # Reset delay after a successful request
        yield response.json(), page
        page += 1


# Function to process and insert topics data
def process_topics_data(json_data, page, session):
    new_count = 0
    topics_data = json_data.get("topic_list", {}).get("topics", [])

    for topic in topics_data:
        try:
            topic_entry = ProtocolTopics(
                id=topic.get("id"),
                slug=topic.get("slug"),
                title=topic.get("title"),
                created_at=datetime.datetime.fromisoformat(
                    topic["created_at"].rstrip("Z")
                )
                if topic.get("created_at")
                else None,
                last_posted_at=datetime.datetime.fromisoformat(
                    topic["last_posted_at"].rstrip("Z")
                )
                if topic.get("last_posted_at")
                else None,
                category_id=topic.get("category_id"),
                posters=topic.get("posters"),
                views=topic.get("views"),
                reply_count=topic.get("reply_count"),
                page=page,
            )
            existing_entry = (
                session.query(ProtocolTopics).filter_by(id=topic_entry.id).one_or_none()
            )
            if not existing_entry:
                session.add(topic_entry)
                new_count += 1
        except Exception as e:
            logging.error(f"Error processing topic {topic.get('id')}: {e}")

    return new_count


# Function to process and insert users data
def process_users_data(json_data, page, session):
    new_count = 0
    users_data = json_data.get("users", [])

    for user in users_data:
        try:
            user_entry = ProtocolUsers(
                id=user.get("id"),
                username=user.get("username"),
                name=user.get("name"),
                trust_level=user.get("trust_level"),
                admin=user.get("admin"),
                moderator=user.get("moderator"),
                page=page,
            )
            existing_entry = (
                session.query(ProtocolUsers).filter_by(id=user_entry.id).one_or_none()
            )
            if not existing_entry:
                session.add(user_entry)
                new_count += 1
        except Exception as e:
            logging.error(f"Error processing user {user.get('id')}: {e}")

    return new_count


# Main function to control the flow
def main():
    start_time = time.time()
    with Session() as session:
        # Topics
        topics_new_count = 0
        for json_data, page in fetch_paginated_data(
            "https://dao.rocketpool.net/top.json?period=all&page={}", 0, session
        ):
            topics_new_count += process_topics_data(json_data, page, session)

        # Users
        users_new_count = 0
        for json_data, page in fetch_paginated_data(
            "https://dao.rocketpool.net/top.json?period=all&page={}", 0, session
        ):
            users_new_count += process_users_data(json_data, page, session)

        session.commit()

    total_time = time.time() - start_time
    logging.info(f"Total new topics added: {topics_new_count}")
    logging.info(f"Total new users added: {users_new_count}")
    logging.info(f"Total time taken for the pipeline: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()

from sqlalchemy import (
    create_engine,
    text,
    select,
    func,
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
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# SQLAlchemy Model
Base = declarative_base()


class ProtocolTopicsPost(Base):
    __tablename__ = "protocol_topics_post_pages"
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
    page = Column(Integer)


# Function to fetch data from a paginated URL
def fetch_paginated_data(base_url, start_page=0):
    page = start_page
    delay = 1  # starting with 1 second delay
    while True:
        paginated_url = f"{base_url}?period=all&page={page}"
        logging.info(f"Fetching data from URL: {paginated_url}")
        response = requests.get(paginated_url)
        if response.status_code == 429:
            logging.warning(f"Rate limit reached, sleeping for {delay} seconds")
            time.sleep(delay)
            delay *= 2  # Double the delay for each retry
            continue

        delay = 1  # Reset delay after successful request
        if response.status_code != 200:
            logging.warning(
                f"Failed to fetch data from {paginated_url}: Status code {response.status_code}"
            )
            break

        json_data = response.json()
        if (
            "errors" in json_data
            and json_data["errors"][0]
            == "The requested URL or resource could not be found."
        ):
            break

        yield json_data, page
        page += 1


# Function to find the most recent page and updated_at timestamp
def get_last_page_and_timestamp(session):
    stmt = select(
        func.max(ProtocolTopicsPost.page), func.max(ProtocolTopicsPost.updated_at)
    )
    result = session.execute(stmt).first()
    return result


# Main function to control the flow
def main():
    start_time = time.time()
    engine = create_engine("sqlite:///rocketpool.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    # session = Session()

    # Create a session for getting the last page and timestamp
    with Session() as temp_session:
        last_page, last_updated_at = get_last_page_and_timestamp(temp_session)
    start_page = 0 if last_page is None else max(last_page - 5, 0)

    new_posts_count = 0
    logging.info("Starting data fetching process")
    with Session() as session:
        # Fetch URLs
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT id, slug FROM protocol_topics_pages")
            )
            urls = [
                f"https://dao.rocketpool.net/t/{row[1]}/{row[0]}.json" for row in result
            ]

        for base_url in urls:
            for json_data, page in fetch_paginated_data(
                base_url, start_page=start_page
            ):
                logging.info(f"Processing data from page {page} of URL {base_url}")
                posts_data = json_data.get("post_stream", {}).get("posts", [])
                for post in posts_data:
                    existing_post = (
                        session.query(ProtocolTopicsPost)
                        .filter_by(id=post["id"])
                        .one_or_none()
                    )

                    if not existing_post:
                        # Insert new post
                        try:
                            new_post_entry = ProtocolTopicsPost(
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
                                page=page,
                            )
                            session.add(new_post_entry)
                            new_posts_count += 1
                            print(f"New post added: ID - {post.get('id')}")
                        except Exception as e:
                            print(f"Error inserting new post data: {e}")

            session.commit()
            # Increment new_posts_count if a new post is added
        session.close()
        print(f"Total new posts added: {new_posts_count}")
        logging.info(f"Total new posts added: {new_posts_count}")
    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f"Total time taken for the pipeline: {total_time:.2f} seconds")


# Execute the main function
if __name__ == "__main__":
    main()

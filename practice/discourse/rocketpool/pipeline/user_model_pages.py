import requests
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLAlchemy Model
Base = declarative_base()


class ProtocolUsers(Base):
    __tablename__ = "protocol_users_pages"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    trust_level = Column(Integer)
    admin = Column(Boolean)
    moderator = Column(Boolean)
    page = Column(Integer)


# SQLAlchemy Engine and Session Setup
engine = create_engine("sqlite:///rocketpool.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Initialize Session
session = Session()

# Loop through pages
page = 0
while True:
    paginated_url = f"https://dao.rocketpool.net/top.json?period=all&page={page}"
    response = requests.get(paginated_url)

    if response.status_code != 200:
        print(
            f"Failed to retrieve data from page {page}: HTTP Status Code {response.status_code}"
        )
        break

    json_data = response.json()
    users_data = json_data.get("users", [])

    if not users_data:
        print(f"No more users found on page {page}.")
        break

    # Extract and insert/update data
    for user_data in users_data:
        # Use .get() to handle missing keys
        user_entry = ProtocolUsers(
            id=user_data.get("id"),
            username=user_data.get("username"),
            name=user_data.get("name"),
            trust_level=user_data.get("trust_level"),
            admin=user_data.get("admin"),
            moderator=user_data.get("moderator"),
            page=page,  # Include the page number
        )
        existing_user = (
            session.query(ProtocolUsers).filter_by(id=user_entry.id).one_or_none()
        )

        if existing_user:
            # Update existing user
            existing_user.username = user_entry.username
            existing_user.name = user_entry.name
            existing_user.trust_level = user_entry.trust_level
            existing_user.admin = user_entry.admin
            existing_user.moderator = user_entry.moderator
            existing_user.page = user_entry.page
        else:
            # Insert new user
            session.add(user_entry)

    # Commit data to the database for each page
    session.commit()

    # Increment page number for next iteration
    page += 1

# Close Session
session.close()

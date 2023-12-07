from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
import requests
import pandas as pd

# SQLAlchemy Model
Base = declarative_base()


class ProtocolCategories(Base):
    __tablename__ = "protocol_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    topic_count = Column(Integer)
    post_count = Column(Integer)
    description = Column(String)
    topic_url = Column(String)


# Create an engine and tables
engine = create_engine("sqlite:///rocketpool.db")
Base.metadata.create_all(engine)

# Fetch Data
url = "https://dao.rocketpool.net/categories.json"
response = requests.get(url)
if response.status_code == 200:
    json_data = response.json()

    # Accessing 'categories' inside categories list
    category_list = json_data.get("category_list", {})
    categories_data = category_list.get("categories", [])
    if not categories_data:
        print("The 'categories' key was not found or is empty.")

    # Process data into a list of dictionaries
    processed_data = []
    for category in categories_data:
        try:
            processed_data.append(
                {
                    "id": category.get("id"),
                    "name": category.get("name"),
                    "slug": category.get("slug"),
                    "topic_count": category.get("topic_count"),
                    "post_count": category.get("post_count"),
                    "description": category.get("description"),
                    "topic_url": category.get("topic_url"),
                }
            )
        except Exception as e:
            print(f"Error processing category {category.get('id')}: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(processed_data)

    # Insert data into database
    Session = sessionmaker(bind=engine)
    session = Session()
    for data_dict in df.to_dict(orient="records"):
        category = ProtocolCategories(**data_dict)
        session.add(category)
    session.commit()
    session.close()
else:
    print("Failed to retrieve data: HTTP Status Code", response.status_code)

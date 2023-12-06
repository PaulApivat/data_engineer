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

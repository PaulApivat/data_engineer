## Rocket Pool Discourse

### Overview

This repo contains exploratory and pipeline related scripts for navigating **Rocket Pool Discourse** data, creating initial data models and an initial pipeline for ingesting data for further processing. There is a SQLite database **rocketpool.db** that contains tables for discourse `categories`, `topics`, `posts` and `users`.

The database is **not** pushed into version control as it contains potentially *confidential* user data. 

The `pipeline` folder contains various scripts for creating SQLalchemy models. 

### Discourse Data

Rocket Pool's discourse forum can filtered by categories, latest or top. 

There are currently 11 categories including: Governance, Liquid Staking Experience, Node Operator Experience, Community, Education, Growth, Integration, Grants / Bounties, Uncategorized and Polls. Selecting the "Categories" tab presents all categories, number of topics within and the latest posts.

Selecting the "Latest" tab presents a list of Topic Posts by recent Activity.

Selecting the "Top" tab presents a list of Topic Posts with the most Views/Replies. By default, the date range is set to showing posts within the last year (as of this writing Dec 7, 2022 - Dec 7, 2023). 

Here's a filter by "Top" topic posts:

![rocketpool_discourse_filters](png/rocketpool_discourse_filters.png)

### JSON 

So far data has been extracted by appending `.json` to the end of a URL for example:

`https://dao.rocketpool.net/top.json`

For initial extraction, I've used the above URL to gather User, Topic and Post data. For Categories, I've used:

`https://dao.rocketpool.net/categories.json`

This allow for an initial dataset filtered by Posts with the most Views/Replies. There are *alternatives* including filter by individual categories...

`https://dao.rocketpool.net/c/liquid-staking-experience/14.json`

...filtering by a single topic (thread)...

`https://dao.rocketpool.net/t/rpl-staking-rework-proposal/2090.json`


...the latest (most recent) posts (even latest within a category)...

`https://dao.rocketpool.net/latest.json`

All depending on **what kind of data is needed for what purpose**. 

### Data Model

Here's a visual database model for Rocket Pool's discourse forum data:

![rocketpool_db_model](png/rocketpool_db_model.png)

continue:

![rocketpool_db_model_2](png/rocketpool_db_model_2.png)

### Creating SQLite database

To create `rocketpool.db`, run the following commands (**note**: order matters where Posts rely on Topic tables for their creation so the `protocol_topics` table should be created before `protocol_topic_posts` table.)

Recommended order:

- category: `python -m category_model`
- topic: `python -m topic_model`
- post: `python -m post_model`
    - note: `create_post_urls.py` is already contained in `post_model.py` (running `post_model.py` first will print out the concatenated post URLs)
- user: `python -m user_model`

### Lack of Native Pagination Support

discourse.org does not support native pagination despite repeated community requests over the years. These links provide background context ([July 2022](https://meta.discourse.org/t/is-pagination-impossible-or-just-hard/231838), [Nov 2023](https://meta.discourse.org/t/pagination-needed-for-post-or-topic-section/284921), [Dec 2023](https://meta.discourse.org/t/infinite-scrolling-on-homepage/288194/5))

Instead, discourse.org favors infinite scrolling. However, when using the `.json` approach for data extraction a web requests can only fetch a limited response. 

### Pagination with Pages

The good news is we can use the `page` parameter to create a **paginated URL**. 

For example, this:

url = f"https://dao.rocketpool.net/top.json"

becomes this:

paginated_url = f"https://dao.rocketpool.net/top.json?period=all&page={page}"

#### Page Index

Using the `page` parameter allows us to create a while-loop through all available page. Paired with the `period=all` parameter, we can get _all_ topics across categories. Currently, we have successful implementation for:

- topics (page index starts at 0)
- topic_posts (page index starts at 1)
- users (same as topic)

### New Data

Now that we have a rough working approach to pagination, we need a way to acquire and insert new data. 
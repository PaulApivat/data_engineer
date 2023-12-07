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

### Options

In terms of data extraction there are two primary options:

1. The `.json` approach

2. Web scraping 

Eventually, we'll likely need to implement an asynchronous approach to collecting data (web scraping), but it may serve us well to start off with the `.json` (and try different variations) to clearly define  what data is **most valuable** for our business or customer acquisition objectives. 
## Project documentation

### Overview 

This repo contains supporting materials for the more conceptual **Data Infra Outline** presentation contained [here](https://docs.google.com/presentation/d/1cTAUfFR9t_07dHk8hT6OyZbTvqPOvzZt-okjWMhd3P4/edit?usp=sharing).

This is a _demo repo_ that shows:

- how a multi-hop data architecture _could_ look like in practice.
- how the metric `eth_emissions` is _progressively transformed_.
- how separation of input/output from transformation in a data pipeline might look like.
- how separate data quality checks at various point of the pipeline might look like including:
    - separate schemas to validate against
    - separate test for each quality check
- exploring different databases and tables with `jupyter notebooks`
- alternatively, exploring different databases and tables with `duckdb`

### Background

This demo focuses on `eth_emissions`. 

An `ETH Overview Meta-Feed` consists of a group of metrics to describe various aspects of Ethereum the protocol, and ETH the asset. Users will gain an understanding how much activity Ethereum the protocol facilitates through metrics like `emissions`, `fees`, `smart contracts deployed (created)`, `daily active users` etc. And correspondingly, users will see how these activity metrics translate into bullish or bearish sentiment around ETH the asset, reflected in price. 

In this example, let’s take `emissions` as raw data, one of several indicators of how much activity Ethereum, the protocol, facilitates. If we were to ingest emissions into a multi-hop architecture, we might have a discussion about what would be interesting for raw data, facts and dimensions; then, finally, what is the actual metric of interest. 

**Declaring the grain to build dimensions and fact tables**

The issuance of ETH is the process of creating ETH that did not previously exist. The burning of ETH is when existing ETH gets destroyed, removing it from circulation.” ([source](https://ethereum.org/en/roadmap/merge/issuance/)). Let’s say for the sake of this contrived example, net emissions is issuance minus burn. It is a statement about ETH supply and it is something that can be tracked daily. That’s the grain of the table. 

**Fact**: `date (datetime)` and `net_emission_eth`
**Dimensions**: token symbol (`ETH`), protocol name (`ethereum`) , category (`eth overview`) , layer (`L1`), relevance (`ETH supply`) 

Declaring facts and dimensions could have direct relevant for meta-data that gets fed into a Prompt. This process will inform the data dictionary, and could help inform prompt guidance.

**Dune Analytics query**: https://dune.com/queries/3032256

### DuckDB

One objective for this repo is to facilitate our diligence process in considering DuckDB as a potential SQLite alternative. 

Installation:

```
$ brew install duckdb
```

Initializing the CLI and exploring a database:

```
#initialize duckdb CLI w specific database name

$ duckdb raw_data.db

# select all existing tables within a database

D SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'; 

# select first 10 rows from a specific table ('eth_emissions') within database (raw_data.db)

D SELECT * FROM eth_emissions LIMIT 10;
```
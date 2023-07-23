
## How should we organize and manage data?

- **schemas**: How should my data be logically organized?
- **normalization**: Should my data have minimal dependency and redundancy?
- **views**: What joins will be done most often?
- **access control**: Should all users of the data have the same level of access?
- **DBMS**: How do I pick between all the SQL and noSQL options?

## Approaches to processing data

- **OLTP**: Online *Transactions* Processing
- **OLAP**: Online *Analytical* Processing

### Examples:

#### OLTP Tasks
- Find price of a a book
- Update latest customer transaction
- Keep track of employee hours
- * Should not be part of data warehouse

#### OLAP Tasks
- Calculate books with the best profit margin
- Find most loyal customers
- Decide employee of the month
- * Purpose is to save historical data and maintain ETL processes for data analysis.


|         | OLTP                                     | OLAP                                           |
|---------|------------------------------------------|------------------------------------------------|
| Purpose | support daily transactions               | report and analyze data                        |
| Design  | application-oriented                     | subject-oriented                               |
| Data    | up-to-date, operational                  | consolidated, historical                       |
| Size    | snapshot, gigabytes                      | archive, terabytes                             |
| Queries | simple transactions and frequent updates | complex, aggregate queries and limited updates |
| Users   | thousands                                | hundreds                                       |


## Working Together

Both are needed:
- OLAP informs that Data Warehouse
- OLTP informs the Operational Database

**Note**: Data that comes out of a blockchain "block" tends to be OLTP in nature. Companies like Dune / Flipside serve as giant Operational Databases, while data analysts might pull a subset of data to store in their Data Warehouse.


## Questions

- What are the business requirements?
- Do we need OLAP, OLTP or both?


## Storing Data

### Structuring Data

1. **Structured Data**
- follows a schema
- defined data types and relationships
- e.g., SQL tables in a relational db

2. **Unstructured Data**
- schema-less
- e.g., photos, chat logs

3. **Semi-structured Data**
- self-describing structure
- e.g., JSON, XML 
- e.g., response object of an API call


### Storing data beyond traditional databases

1. **Traditional Databases**
- real-time relational structured data
- OLTP

2. **Data warehouses**
- analyzing archive structured data
- OLAP

3. **Data Lakes**
- stores data of all structures
- analyzing big data


### Data warehouses

- Optimized for analytics - OLAP
- Contains data from multiple sources
- Massively Parallel Processing (MPP)
- Typically uses a *denormalized schema* and dimensional modeling

- * Denormalizing is hte process of adding precomputed _redundant_ data to an otherwise normalized relational database to improve read performance.
- * Denormalizing a database requires data has first been normalized. 

#### Data Marts

- subset of data warehouse
- dedicated to a specific topic

#### How will data get to to storage?

- **ETL**: Extract to staging; Transform, the Load to Data Warehouse; schema predefined for usage.

- **ELT** Extract and Load to a Data Lake (in raw natural form), then Transform for specific use case.

## What is Database Design?

- Determines how data is logically stored
- How is data going to be read and updated?

- Uses **database models**: Most popular - Relational model
- other options: NoSQL, objected oriented, network model
- Uses **schemas**: blueprint of database
- define tables, fields, relationships, indexes and views
- when inserting data in a relational database, schemas must be respected

### Data Modeling

**Process of creating a data model for the data to be stored**

1. **Conceptual data model**: describes entities, relationships and attributes
- *Tools* data structure diagrams e.g., UML diagrams
2. **Logical data model**: define tables, columns, relationships 
- *Tools*: database model and schemas e.g., relational model and star schema
3. **Physical data model**: describes physical storage
- *Tools*: partitions, CPUs, indexes, backup systems and tablespaces

### Elements of Dimensional Modeling

#### Fact Tables

- Decided by business use-case
- Holds records of a metric
- Changes regularly
- Connects to dimension via foreign keys

#### Dimension Tables

- Holds description of attributes
- Does not change as often

* Consider what is being analyzed and how often it changes.



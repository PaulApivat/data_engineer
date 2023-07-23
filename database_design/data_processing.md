
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



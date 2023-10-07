## Downstream Data - ETL
### Handling third party data via Workers (Celery) and API Calls to Dune Analytics

Referencing this [article](https://adamparrish.xyz/downstream-data-extract-transform-load) with specific adjustments.

### Project Structure

```
project_root/
│
├── etl/
│   ├── __init__.py
│   ├── config.py  # your configuration settings
│   │
│   ├── common/
│   │   ├── __init__.py
│   │   ├── model/
│   │   │   ├── __init__.py
│   │   │   |--- db/
|   |   |   |   |── __init__.py
│   │   │   ├   |── etl_reference_master_model.py  # contains DigitalAssetMetric
|   |   |   |   |-- database_init.py 
|   |   |   |   |-- insertion_test.py
|   |   |   |   |-- bronze.db 
|   |   |   |   |-- raw_model.py # ensure DigitalAssetMetric entries are inserted before RecordedRawMetric.
│   │   │   └── ...
│   │   └── ...
│   │
│   ├── periodic/
│   │   ├── __init__.py
│   │   ├── celery_config.py  # celery configuration
│   │   └── ...
│   │
│   ├── client/
│   │   ├── __init__.py
│   │   ├── dune_wrapper.py  # contains your logic to interact with Dune Wrapper
│   │   └── ...
│   │
│   └── tasks/   # celery tasks
│       ├── __init__.py
│       ├── onchain_tasks.py
│       └── ...
│
├── k8s/
│   ├── foliofficient-onchain-worker-deployment.yaml  # Kubernetes deployment file
│   ├── configmap/  # Kubernetes ConfigMap manifests
│   │   ├── foliofficient-app-config.yaml
│   │   └── foliofficient-worker.yaml
│   └── ...
│
├── logs/  # for logging
│
├── Dockerfile  # to build docker image for Kubernetes
│
├── requirements.txt  # python dependencies
│
└── README.md  # documentation on how to set up, run, and contribute to your project

```

### Project Description

**etl/**: This is the core of the application where all Python modules reside. This structure helps keep the application modular and maintainable.

**config.py**: Contains configuration settings.
**common/**: Shared utilities, models, and functions.
**periodic/**: Holds the celery-related modules and configurations.
**client/**: Contains API clients or wrappers.
**tasks/**: Celery tasks.
**k8s/**: Contains Kubernetes manifests.

**configmap/**: Kubernetes ConfigMap manifests.
**logs/**: A directory to optionally store logs, though in a Kubernetes environment, consider using a centralized logging system.

**Dockerfile**: Defines the container image for the application, which will be used in Kubernetes.

**requirements.txt**: Lists all the Python dependencies for the project.

### Initial Procedures

1. unittest for Dune Client `python -m etl.client.dune_wrapper`

Now that we can get the data out of Dune, we want to load the data into a SQLite database.

1. initialize database `python -m etl.common.model.db.database_init`
2. test data insertion `python -m etl.common.model.db.insertion_test`
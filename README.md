# Automated Open Data Harvesting

This project automates the harvesting and visualization of open data using Docker Compose.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

To start the containers defined in `docker-compose.yml`:
```sh
    docker-compose up
```

To start the containers in detached mode:

```sh
    docker-compose up -d
```

To build and start the containers:

```sh
    docker-compose up --build
```

### Stopping the Application

To stop the containers started with `docker-compose up`:

```sh
    docker-compose down
```

### Viewing Logs

To view the logs of the containers:

```sh
    docker-compose logs [SERVICE_NAME]
```

Replace `[SERVICE_NAME]` with the name of the specific service you want to check the logs for.

## Project Structure

```sh
    .
    ├── README.md
    └── web-server
        ├── automated_harvesting
        │   ├── admin.py
        │   ├── apps.py
        │   ├── forms.py
        │   ├── urls.py
        │   ├── models
        │   ├── templates
        │   ├── templatetags
        │   ├── utils
        │   └── views
        ├── automated_open_data_harvesting
        │   ├── asgi.py
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        ├── automated_open_data_harvesting_env
        ├── database
        │   ├── create_database.sql
        │   └── populate.sql
        ├── docker-compose.yml
        ├── Dockerfile
        ├── manage.py
        ├── requirements.txt
        └── static
            ├── admin
            └── automated_harvesting
```

- `templates/`: This directory contains HTML templates used for rendering the web pages of the application.
  - `actions/`: Contains templates for performing various actions such as adding or modifying records.
  - `datasets_views/`: Templates specifically related to displaying and interacting with datasets.
  - `model_views/`: Templates for viewing and interacting with different data models.

- `templatetags/`: Contains custom template filters and tags used to extend the template language.
  - `custom_filters.py`: Defines custom template filters that can be used in HTML templates to manipulate and display data.

- `utils/`: A collection of utility modules that provide various helper functions and classes.
  - `data_parsing/`: Scripts for parsing different data formats such as CSV, DBF, ODS, SHP, XLS, and XLSX.
  - `datasets/`: Contains scripts for handling dataset-related operations, such as downloading datasets.
  - `db_operations.py`: Provides utility functions for performing database operations.
  - `url_handler.py`: Utilities for handling and processing URLs.

- `views/`: This directory includes view functions responsible for handling web requests and returning responses.
  - `analyse_view.py`: Contains the view logic for analyzing data.
  - `base_view.py`: Base view functions that provide common functionality used across multiple views.
  - `datasets_views.py`: Handles the views related to datasets, such as displaying dataset information.
  - `data_table_view.py`: Manages views for displaying and interacting with data tables.
  - `model_views.py`: Contains views for displaying and managing different data models.
  - `url_table_mapping_view.py`: Handles the view for mapping URLs to specific data tables.

  ## Dynamic Data Management

Once the data is downloaded, users can specify which columns are static and which are dynamic. This is useful for handling time-series data or any data that changes over time.

### Example: Managing Meteo Data

Consider a dataset containing weather information with the following columns:
- `Place`
- `Date`
- `Temperature`

#### Step 1: User Defines Static and Dynamic Columns

The user selects `Place` as the static column and `Date` and `Temperature` as the dynamic columns.

#### Step 2: Creating Static and Dynamic Tables

The system will create two tables:
- `meteo_s`: Contains static data with the column `Place`.
- `meteo_d`: Contains dynamic data with columns `static_id`, `Date`, and `Temperature`.

#### Step 3: Populating the Tables

For data entries like `Bayonne, 2024/06/28, 18°` and `Biarritz, 2024/06/28, 20°`, the following records will be created:

- In `meteo_s`:
    - `1, Bayonne`
    - `2, Biarritz`

- In `meteo_d`:
    - `1, 1, 2024/06/28, 18` (static_id 1 refers to Bayonne)
    - `2, 2, 2024/06/28, 20` (static_id 2 refers to Biarritz)

#### Example with New Data

When new data is added, such as `Bayonne, 2024/06/29, 15°` and `Biarritz, 2024/06/29, 19°`, the tables will be updated as follows:

- `meteo_s` remains unchanged because the static data (`Bayonne` and `Biarritz`) are already present:
    - `1, Bayonne`
    - `2, Biarritz`

- `meteo_d` will be updated to include the new dynamic data:
    - `1, 1, 2024/06/28, 18`
    - `2, 2, 2024/06/28, 20`
    - `3, 1, 2024/06/29, 15`
    - `4, 2, 2024/06/29, 19`

#### Step 4: Creating a View for Easier Access

To simplify data access, a view `meteo_view` is created to join the static and dynamic tables. This view combines the information for easier querying:

- `meteo_view`:
    - `Place, Date, Temperature`

The `meteo_view` will look like this:

| Place    | Date       | Temperature |
|----------|------------|-------------|
| Bayonne  | 2024/06/28 | 18°         |
| Biarritz | 2024/06/28 | 20°         |
| Bayonne  | 2024/06/29 | 15°         |
| Biarritz | 2024/06/29 | 19°         |

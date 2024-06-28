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


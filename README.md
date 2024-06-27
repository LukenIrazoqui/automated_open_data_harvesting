# automated_open_data_harvesting
Python project for the automated harvesting and visualisation of open data

Running Docker Compose:
	To start containers defined in docker-compose.yml:
		docker-compose up

	To start containers in detached mode:
		docker-compose up -d

	To build and start containers:
		docker-compose up --build

Stopping Docker Compose:
	To stop containers started with docker-compose up:
		docker-compose down

Viewing Logs:	
	To view logs of containers started with Docker Compose:
		docker-compose logs [SERVICE_NAME]

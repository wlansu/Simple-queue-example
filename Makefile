# Makefile

# Build the Docker containers
build:
	docker-compose build

# Start the Docker containers
up:
	docker-compose up -d

# Stop the Docker containers
down:
	docker-compose down

# Run tests inside the Django container
test:
	docker-compose run django bash -c "PYTHONPATH=/usr/src/app pytest -vv"

lint:  ## Run all the linters
	docker-compose run django poetry run ruff format /usr/src/app
	docker-compose run django poetry run mypy /usr/src/app

# Call the endpoints
create_timer:
	curl -s -w "\n" -X POST http://0.0.0.0:8000/timer \
		-H "Content-Type: application/json" \
		-d '{"hours": $(HOURS), "minutes": $(MINUTES), "seconds": $(SECONDS), "url": "$(URL)"}'

retrieve_timer:
	open http://0.0.0.0:8000/timer/$(TIMER_UUID)

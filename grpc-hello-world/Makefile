.PHONY: build up down restart logs logs-server logs-client client-logs ps clean

# Build both images (regenerates the pb2 stubs from proto/ during build).
build:
	docker compose build

# Start the server, then run the client against it (client exits after one call).
up:
	docker compose up --build

# Same as up, but detached; use `make logs` to follow output.
up-d:
	docker compose up --build -d

down:
	docker compose down

restart: down up

logs:
	docker compose logs -f

logs-server:
	docker compose logs -f server

logs-client:
	docker compose logs -f client

ps:
	docker compose ps

# Remove containers, networks, and images built by this compose file.
clean:
	docker compose down --rmi local -v

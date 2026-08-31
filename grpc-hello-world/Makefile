# Docker compose app -- maps the shared verbs onto compose, plus a few extras.

include ../make/common.mk

COMPOSE := docker compose

.PHONY: up down logs logs-server logs-client ps

install:            ## build both images (regenerates pb2 stubs from proto/)
	$(COMPOSE) build

run:                ## start server, then the client against it
	$(COMPOSE) up --build

up-d:               ## same as run, detached
	$(COMPOSE) up --build -d

down:               ## stop the stack
	$(COMPOSE) down

logs:               ## follow all logs
	$(COMPOSE) logs -f

logs-server:
	$(COMPOSE) logs -f server

logs-client:
	$(COMPOSE) logs -f client

ps:                 ## show container status
	$(COMPOSE) ps

clean:              ## remove containers, networks, and images built here
	$(COMPOSE) down --rmi local -v

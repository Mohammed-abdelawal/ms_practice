# Serverless app -- functions run under osls (the open-source Serverless
# Framework) and serverless-offline, which emulate API Gateway + Lambda over
# plain HTTP. That part lives entirely in docker.
#
# Real deploy runs on the host instead (so it can see your own AWS creds),
# and osls needs Node >=20.19/22.13/24 -- newer than this host's system node.
# So `deploy`/`remove` fetch a pinned Node 22 into .envs/, same pattern
# nodejs_app and flask_app use for their own toolchains.

include ../make/common.mk

COMPOSE      := docker compose
URL          := http://localhost:4000
EVENT        := '{"queryStringParameters": {"name": "invoke"}}'
STAGE        := dev
NODE_VERSION := 22.23.2
NODE_DIST    := node-v$(NODE_VERSION)-linux-x64
NODE_HOME    := $(ENV)/$(NODE_DIST)
NPM_BIN      := $(NODE_HOME)/bin/npm
# npm/npx are `#!/usr/bin/env node` scripts, so calling them by absolute path
# still resolves `node` from PATH -- it has to be put in front for real.
WITH_NODE    := PATH="$(NODE_HOME)/bin:$$PATH"
NPM          := $(WITH_NODE) $(NPM_BIN)
NPX          := $(WITH_NODE) $(NODE_HOME)/bin/npx

install:            ## build the image (osls, serverless-offline, python3)
	$(COMPOSE) build

run:                ## serve the functions on :4000, handler edits apply live
	$(COMPOSE) up --build

# --wait blocks until the healthcheck passes. Without it, docker's port proxy
# accepts connections before the emulator listens and answers with nothing.
up-d:               ## same as run, detached; returns once it is listening
	$(COMPOSE) up --build -d --wait

down:               ## stop the emulator
	$(COMPOSE) down

logs:               ## follow the emulator's output
	$(COMPOSE) logs -f

call:               ## hit both functions over HTTP (needs run or up-d)
	@curl -s "$(URL)/hello/node?name=make"; echo
	@curl -s "$(URL)/hello/python?name=make"; echo

invoke:             ## call both handlers directly, skipping the HTTP layer
	$(COMPOSE) run --rm offline npx osls invoke local -f helloNode --data $(EVENT)
	$(COMPOSE) run --rm offline npx osls invoke local -f helloPython --data $(EVENT)

clean:              ## remove containers, the image built here, and host deploy tooling
	$(COMPOSE) down --rmi local -v
	rm -rf $(ENV) node_modules

$(NPM_BIN):
	@mkdir -p $(ENV)
	curl -fsSL https://nodejs.org/dist/v$(NODE_VERSION)/$(NODE_DIST).tar.xz | tar -xJ -C $(ENV)

# node_modules sits directly in this dir (not relinked from .envs/, unlike
# nodejs_app) because it's already gitignored and osls/npx need it right next
# to package.json to find the local osls binary.
node_modules: $(NPM_BIN)
	$(NPM) install --no-audit --no-fund

deploy: node_modules ## deploy functions to AWS (host, needs your own AWS creds)
	$(NPX) osls deploy --stage $(STAGE)

remove: node_modules ## tear down the deployed AWS stack
	$(NPX) osls remove --stage $(STAGE)

.PHONY: up-d down logs call invoke deploy remove

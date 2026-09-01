# Node app -- node_modules kept in .envs/nodejs_app/, symlinked back in here.
#
# Node resolves `require('express')` by looking for a directory literally named
# node_modules next to server.js, so the symlink has to exist; the packages
# themselves live in .envs/. npm always rebuilds a real node_modules next to
# package.json, so install relocates it afterwards and re-links.

include ../make/common.mk

install:            ## npm install, with node_modules parked in .envs/
	@[ -f package.json ] || { echo "$(APP_NAME)/ has no package.json"; exit 1; }
	npm install
	@mkdir -p $(ENV)
	@rm -rf $(ENV)/node_modules
	@mv node_modules $(ENV)/node_modules
	@$(MAKE) --no-print-directory link
	@echo "ready: $(ENV)/node_modules"

# Recreated on demand: a missing or dangling link is just relinked, not an error.
link: | $(ENV)/node_modules
	@rm -f node_modules
	@ln -s ../.envs/$(APP_NAME)/node_modules node_modules

$(ENV)/node_modules:
	@echo "no env yet -- run: make install $(APP_NAME)"; exit 1

run: link           ## serve, restarting on file changes (node --watch)
	npm run dev

start: link         ## serve once, no watcher
	npm run start

clean:              ## remove node_modules and the symlink
	rm -rf $(ENV)
	@[ -L node_modules ] && rm -f node_modules || true

.PHONY: link start

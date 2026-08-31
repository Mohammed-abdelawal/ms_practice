# Paths + help, shared by every app Makefile. No recipes live here -- each app
# writes its own install/run/clean, they just agree on the same target names.
#
# ROOT comes from this file's own path, so an app Makefile works both from the
# repo root (make run APP=x) and from inside the app dir (cd x && make run).

ROOT     := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))..)
APP_NAME := $(notdir $(CURDIR))
ENVS     := $(ROOT)/.envs
ENV      := $(ENVS)/$(APP_NAME)

.DEFAULT_GOAL := help
.PHONY: help install run clean

# Self-documenting: lists every `target: ## description` in this app's Makefile.
help:
	@echo "$(APP_NAME):"
	@grep -hE '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##/|/' | \
		sort | awk -F'|' '{ printf "  %-12s %s\n", $$1, $$2 }'

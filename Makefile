# Dispatcher only -- every app owns its own Makefile and writes its own
# install/run/clean. They just agree on the same target names; this forwards.
#
#   make install nodejs_app        \  same thing -- name the app either way
#   make install APP=nodejs_app    /
#   make nodejs_app                shorthand for run
#   make help nodejs_app           what that app can do, incl. its own extras
#   make install-all               every app
#
# Anything not defined here is forwarded too, so an app-specific target (say
# `make shell flask_app`) works without touching this file.
#
# Envs (venvs, node_modules) all live in .envs/<app>/ and are gitignored.

ENVS := .envs
APPS := $(patsubst %/Makefile,%,$(wildcard */Makefile))

# A bare app name among the goals selects the app; APP= still works.
APP_GOAL  := $(lastword $(filter $(APPS),$(MAKECMDGOALS)))
VERB_GOAL := $(filter-out $(APPS),$(MAKECMDGOALS))
APP ?= flask_app
ifneq ($(APP_GOAL),)
  APP := $(APP_GOAL)
endif

FORWARD = $(MAKE) --no-print-directory -C

.DEFAULT_GOAL := usage
.PHONY: usage install run clean help install-all clean-all $(APPS)

usage:
	@echo "usage: make <target> <app>            e.g. make install nodejs_app"
	@echo "       make <target> APP=<app>        equivalent"
	@echo ""
	@echo "  install / run / clean    forwarded to <app>/Makefile"
	@echo "  help                     what a specific app can do"
	@echo "  install-all              install every app"
	@echo "  clean-all                wipe $(ENVS)/ entirely"
	@echo ""
	@echo "apps: $(APPS)"
	@echo "shorthand: make <app> runs it (e.g. make nodejs_app)"

# The shared verbs.
install run clean help:
	@$(FORWARD) $(APP) $@

# Anything else -- an app's own targets -- gets forwarded as well.
.DEFAULT:
	@$(FORWARD) $(APP) $@

# A bare app name means "run it" -- but when a verb was also given it has
# already selected the app above, so here it is just a no-op.
ifeq ($(VERB_GOAL),)
$(APPS):
	@$(FORWARD) $@ run
else
$(APPS): ; @:
endif

# Keeps going if one app isn't set up yet, but still exits non-zero.
install-all:
	@rc=0; for a in $(APPS); do \
		echo "==> $$a"; $(FORWARD) $$a install || rc=1; \
	done; exit $$rc

clean-all:
	@for a in $(APPS); do $(FORWARD) $$a clean; done
	rm -rf $(ENVS)/*/

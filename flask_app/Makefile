# Flask app -- python venv, kept in .envs/flask_app/

include ../make/common.mk

PY        := $(ENV)/bin/python
PIP       := $(ENV)/bin/pip
FLASK     := $(ENV)/bin/flask
FLASK_APP ?= app
PORT      ?= 5000

install:            ## create the venv and install requirements.txt
	@[ -x $(PY) ] || python3 -m venv $(ENV)
	@$(PIP) install -q --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "ready: $(ENV)"

run:                ## serve with the flask dev server (PORT=5000)
	@[ -x $(FLASK) ] || { echo "no env yet -- run: make install"; exit 1; }
	$(FLASK) --app $(FLASK_APP) run --port $(PORT)

dev:                ## same as run, with reloader + debugger
	@[ -x $(FLASK) ] || { echo "no env yet -- run: make install"; exit 1; }
	$(FLASK) --app $(FLASK_APP) run --port $(PORT) --debug

shell:              ## drop into a python repl with the venv
	@$(PY)

clean:              ## remove the venv
	rm -rf $(ENV)

PYTHON := env/bin/python
PIP := $(PYTHON) env/bin/pip

PYTHONUNBUFFERED=1

TEST_DATABASE_URI ?= postgres://testapp:testapp@localhost:15433/testapp

.PHONY: env
env:
	virtualenv -p python3 env
	$(PIP) install -U pip
	$(PIP) install -r requirements.dev.txt

test-db-start:
	docker-compose up -d test-db

test-db-stop:
	docker-compose kill test-db

test:
	DATABASE_URI=$(TEST_DATABASE_URI) \
	    PYTHONPATH=. \
	    env/bin/pytest -v tests

run:
	DATABASE_URI=postgres://app:app@localhost:15432/app $(PYTHON) ./main.py

docker-run:
	docker-compose build app
	docker-compose up app

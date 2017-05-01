PYTHON := env/bin/python
PIP := $(PYTHON) env/bin/pip

PYTHONUNBUFFERED=1

TEST_DATABASE_URI ?= postgres://testapp:testapp@localhost:15433/testapp

.PHONY: env
env:
	virtualenv -p python3 env
	$(PIP) install -U pip
	$(PIP) install -r requirements.dev.txt

.PHONY: test-db-start
test-db-start:
	docker-compose up -d test-db

.PHONY: test-db-stop
test-db-stop:
	docker-compose kill test-db

.PHONY: test
test:
	DATABASE_URI=$(TEST_DATABASE_URI) \
	    PYTHONPATH=. \
	    env/bin/pytest -v tests

.PHONY: run
run:
	DATABASE_URI=postgres://app:app@localhost:15432/app $(PYTHON) ./main.py

.PHONY: docker-run
docker-run:
	docker-compose build app
	docker-compose up app

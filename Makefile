PYTHON := env/bin/python
PIP := $(PYTHON) env/bin/pip

.PHONY: env
env: 
	virtualenv -p python3 env
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt



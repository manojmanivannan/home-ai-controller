.PHONY: venv run

SHELL := /bin/bash
VENV_DIR = venv
REQ_FILE = requirements.txt


venv:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r $(REQ_FILE)
	@echo "Virtual environment setup complete. To activate, run: source $(VENV_DIR)/bin/activate"

run:
	docker compose up --build -d

stop:
	docker compose down --remove-orphans --volumes

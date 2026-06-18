VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: all venv install lint lint-strict clean dev-deps

all: install

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

venv: $(VENV)/bin/activate

install: venv
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) fly_in.py map.txt

debug: install
	$(PYTHON) -m pdb fly_in.py map.txt

dev-deps: install
	$(PIP) install mypy flake8

lint: install dev-deps
	$(PYTHON) -m flake8 . --exclude '$(VENV)'
	$(PYTHON) -m mypy .

lint-strict: install dev-deps
	$(PYTHON) -m flake8 . --exclude '$(VENV)'
	$(PYTHON) -m mypy . --strict

clean:
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)

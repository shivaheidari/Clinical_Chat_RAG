PY=python3
PIP=pip3

PY_FILES := $(shell git ls-files '*.py')

.PHONY: all lint typecheck flake8 pylint mypy install-dev clean

all: lint typecheck

lint: flake8 pylint

typecheck: mypy

flake8:
	$(PY) -m flake8 .

pylint:
	$(PY) -m pylint $(PY_FILES)

mypy:
	$(PY) -m mypy . --ignore-missing-imports

install-dev:
	@echo "Installing development tools (flake8, pylint, mypy)..."
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade flake8 pylint mypy

clean:
	@echo "Removing __pycache__ and .mypy_cache"
	-find . -type d -name "__pycache__" -prune -exec rm -rf '{}' + || true
	-test -d .mypy_cache && rm -rf .mypy_cache || true

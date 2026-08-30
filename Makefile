# Makefile for ItinerPic Python project

.PHONY: help venv install clean lint format test coverage run generate docs

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
BLACK := $(VENV)/bin/black
FLAKE8 := $(VENV)/bin/flake8

help:
	@echo "ItinerPic Python Project - Available targets:"
	@echo ""
	@echo "  make venv          Create virtual environment"
	@echo "  make install       Install dependencies"
	@echo "  make clean         Clean up generated files and cache"
	@echo "  make lint          Run code quality checks"
	@echo "  make format        Format code with Black"
	@echo "  make test          Run test suite"
	@echo "  make coverage      Generate coverage report"
	@echo "  make generate      Run the summary generator"
	@echo "  make all           Setup, install, lint, and test"
	@echo ""

venv:
	python -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"

clean:
	rm -rf build dist .egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache .coverage htmlcov

lint: install
	$(FLAKE8) src tests scripts --max-line-length=100 --ignore=E203,W503
	@echo "Linting passed ✓"

format: install
	$(BLACK) src tests scripts --line-length=100
	@echo "Code formatted ✓"

test: install
	$(PYTEST) tests -v

coverage: install
	$(PYTEST) tests --cov=src --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/"

generate: install
	$(PYTHON) scripts/generate_summaries.py

all: clean install format lint test
	@echo "All checks passed! ✓"

# Development workflow
dev: install
	@echo "Development environment ready. Run 'make generate' to generate summaries."

.DEFAULT_GOAL := help

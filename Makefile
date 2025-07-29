# Makefile for Vyakarana package development

.PHONY: help test test-verbose install install-dev clean lint format

help:
	@echo "Available targets:"
	@echo "  test         - Run tests using the standalone test runner"
	@echo "  test-verbose - Run tests with verbose output"
	@echo "  test-pytest  - Run tests using pytest (requires pytest installation)"
	@echo "  install      - Install the package in development mode"
	@echo "  install-dev  - Install package with development dependencies"
	@echo "  clean        - Remove build artifacts and cache files"
	@echo "  lint         - Run basic linting (if tools are available)"
	@echo "  format       - Format code (if tools are available)"

test:
	python3 tests/test_sutras.py

test-verbose:
	python3 tests/run_tests.py

test-pytest:
	pytest tests/ -v

install:
	pip install -e .

install-dev:
	pip install -e .[dev]

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ 2>/dev/null || true

lint:
	@command -v flake8 >/dev/null 2>&1 && flake8 vyakarana/ tests/ || echo "flake8 not installed"
	@command -v mypy >/dev/null 2>&1 && mypy vyakarana/ || echo "mypy not installed"

format:
	@command -v black >/dev/null 2>&1 && black vyakarana/ tests/ || echo "black not installed"
	@command -v isort >/dev/null 2>&1 && isort vyakarana/ tests/ || echo "isort not installed"

# Show package info
info:
	@echo "Package: Vyakarana"
	@echo "Description: Sanskrit Grammar Python Package"  
	@echo "Python files:"
	@find vyakarana/ -name "*.py" | wc -l | xargs echo "  vyakarana/:"
	@find tests/ -name "*.py" | wc -l | xargs echo "  tests/:"
	@echo "Data files:"
	@find . -name "*.txt" -o -name "*.json" | grep -v __pycache__ | wc -l | xargs echo "  total:"

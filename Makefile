.PHONY: help setup run format clean test test-coverage lint pre-commit release

# Python settings
PYTHON := venv/bin/python
PIP := venv/bin/pip
PYTEST := venv/bin/pytest

# Test directories
TEST_REPORTS_DIR := test-reports
TEST_XML_DIR := $(TEST_REPORTS_DIR)/xml
TEST_HTML_DIR := $(TEST_REPORTS_DIR)/html
COVERAGE_DIR := $(TEST_REPORTS_DIR)/coverage

# Source directories
SRC_DIRS := streamlite_app.py util tests

# Version extraction from CHANGELOG.md
VERSION = 0.0.1

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup         - Install dependencies"
	@echo "  make run          - Run Streamlit app"
	@echo "  make format       - Format code with black and isort"
	@echo "  make lint         - Run code quality checks"
	@echo "  make test         - Run tests"
	@echo "  make test-coverage - Run tests with coverage"
	@echo "  make clean        - Clean up cache files"
	@echo "  make pre-commit   - Run all pre-commit checks"
	@echo "  make release      - Create a new release tag"

# Setup development environment
setup:
	$(PIP) install -r requirements.txt
	pre-commit install

# Run application
run:
	$(PYTHON) -m streamlit run streamlite_app.py

# Format code
format:
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

# Lint code
lint:
	@echo "Running code quality checks..."
	$(PYTHON) -m flake8 $(SRC_DIRS)

# Run tests
test:
	@mkdir -p $(TEST_XML_DIR) $(TEST_HTML_DIR)
	$(PYTEST) -v --junitxml=$(TEST_XML_DIR)/test-results.xml --html=$(TEST_HTML_DIR)/report.html

# Run tests with coverage
test-coverage:
	@mkdir -p $(COVERAGE_DIR)
	$(PYTEST) --cov=. --cov-report=html:$(COVERAGE_DIR) --cov-report=term-missing

# Clean up cache files
clean:
	@echo "Cleaning up cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf $(TEST_REPORTS_DIR)
	rm -rf .coverage htmlcov
	@echo "Cleanup complete!"

# Pre-commit checks
pre-commit:
	@echo "Running pre-commit checks..."
	@echo "1. Code formatting..."
	@make format
	@echo "\n2. Linting..."
	@make lint
	@echo "\n3. Running tests..."
	@make test
	@echo "\n4. Checking test coverage..."
	@make test-coverage
	@echo "\nPre-commit checks completed!"

# Create release tag
release:
	@echo "Creating release v$(VERSION)..."
	@make pre-commit || { echo "Pre-commit checks failed. Fix issues before releasing."; exit 1; }
	@git tag v$(VERSION)
	@echo "Release v$(VERSION) created!"
	@echo "Pushing release to origin..."
	@git push origin v$(VERSION)
	@echo "Release pushed to origin!"

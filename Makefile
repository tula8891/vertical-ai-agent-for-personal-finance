.PHONY: help setup run format clean test test-coverage lint pre-commit release get-version test-imports force-commit dashboard

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

# Default target
help:
	@echo "Demo_app Makefile Commands:"
	@echo ""
	@echo "Development Commands:"
	@echo "  make setup         - Install dependencies and set up development environment"
	@echo "  make run          - Run Streamlit application locally"
	@echo "  make test-imports - Test all required package imports"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  make format       - Format code with black and isort"
	@echo "  make lint         - Run flake8 code quality checks"
	@echo "  make pre-commit   - Run all pre-commit checks (format, lint, test)"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test         - Run tests with HTML and XML reports"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo ""
	@echo "Release Commands:"
	@echo "  make get-version  - Get next version number based on git tags"
	@echo "  make release      - Create and push a new release (VERSION=x.y.z optional)"
	@echo ""
	@echo "Maintenance Commands:"
	@echo "  make clean        - Clean up cache files and test reports"
	@echo ""
	@echo "Example: make release VERSION=1.7.1  # Create release with specific version"

# Setup development environment
setup:
	$(PIP) install -r requirements.txt
	pre-commit install

# Run application
run:
	$(PYTHON) -m streamlit run streamlite_app.py

# Run the evaluation dashboard
dashboard:
	$(PYTHON) -m streamlit run evaluation_dashboard.py

# Test imports
test-imports:
	$(PYTHON) test_imports.py

# Format code
format:
	# $(PYTHON) -m black .
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

# Run pre-commit checks and return status
check-release:
	@echo "Running pre-commit checks..."
	@make pre-commit > /dev/null 2>&1 && echo "success" || ( \
		echo "failed"; \
		echo "\n❌ Pre-commit checks failed. Here are the details:"; \
		make pre-commit; \
		exit 1 \
	)

# Create release tag
release:
	@echo "Determining version number..."
	$(eval NEW_VERSION := $(shell $(MAKE) get-version))
	@echo "Creating release v$(NEW_VERSION)..."
	$(eval CHECK_RESULT := $(shell $(MAKE) check-release))
	@if [ "$(CHECK_RESULT)" = "failed" ]; then \
		echo "❌ Release aborted due to pre-commit check failures."; \
		exit 1; \
	fi
	@echo "✅ Pre-commit checks passed!"
	@echo "Committing changes..."
	@git add .
	@git commit -m "Release v$(NEW_VERSION)" || true
	@echo "Pushing code changes..."
	@git push origin main || { echo "❌ Failed to push code changes. Please resolve any conflicts and try again."; exit 1; }
	@git tag v$(NEW_VERSION) || { echo "❌ Failed to create tag. Tag might already exist."; exit 1; }
	@echo "Release v$(NEW_VERSION) created!"
	@echo "Pushing release tag to origin..."
	@git push origin v$(NEW_VERSION) || { echo "❌ Failed to push tag. Please check remote permissions."; exit 1; }
	@echo "✅ Release v$(NEW_VERSION) completed successfully!"

# Get the latest version tag and increment it
get-version:
	@if [ -z "$(VERSION)" ]; then \
		LATEST_TAG=$$(git describe --tags `git rev-list --tags --max-count=1` 2>/dev/null || echo "v0.0.0"); \
		MAJOR=$$(echo $$LATEST_TAG | cut -d. -f1 | tr -d 'v'); \
		MINOR=$$(echo $$LATEST_TAG | cut -d. -f2); \
		PATCH=$$(echo $$LATEST_TAG | cut -d. -f3); \
		NEW_PATCH=$$((PATCH + 1)); \
		echo "$$MAJOR.$$MINOR.$$NEW_PATCH"; \
	else \
		echo "$(VERSION)"; \
	fi

# Force commit (skip pre-commit hooks)
force-commit:
	SKIP=flake8,black,mypy,trailing-whitespace git commit -m "$(shell git log -1 --pretty=%B)"

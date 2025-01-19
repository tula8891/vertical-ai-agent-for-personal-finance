# Demo_app

## Overview
Demo_app is a Streamlit application that integrates with Snowflake Cortex to provide an interactive chatbot experience. It features a modern landing page, user authentication, and AI-powered financial assistance.

## Features
- **Modern Landing Page**:
  - Clean and intuitive navigation with sidebar menu
  - Section-specific content areas with emoji icons:
    - 📚 Financial Literacy
    - 💰 Investment Recommendations
    - 🤖 AI Agents
  - Quick access navigation menu
  - Responsive design with consistent styling
  - Enhanced button design and alignment
  - Optimized content organization
- **User Interface**:
  - Sidebar navigation with quick access to all features
  - Consistent color scheme across components
  - Modern button styling with hover effects
  - Responsive layout for all screen sizes
  - Enhanced spacing and component alignment
  - Custom font settings for improved readability
- **User Authentication**:
  - Secure login and signup functionality
  - Enhanced email validation and password confirmation
  - Improved error messaging
  - Optimized session state management
- **Interactive Chatbot**: Engage with a chatbot powered by Snowflake Cortex and Mistral LLM
- **Multiple LLM Models**: Support for various models including:
  - mistral-large2
  - llama3.1-70b
  - llama3.1-8b
- **Advanced Search**: Semantic search capabilities using Snowflake Cortex with configurable columns and filters
- **Chat History**: Intelligent context management with configurable history length
- **Theme Configuration**: Customizable UI theme through `.streamlit/config.toml`:
  - Primary color: #4B8BBE
  - Background color: #F0F2F6
  - Secondary background: #FFFFFF
  - Text color: #31333F
  - Custom font settings

## Project Structure
```
Demo_app/
├── .streamlit/          # Streamlit configuration
│   ├── config.toml     # Theme and layout settings
│   └── secrets.toml    # Secure credentials
├── tests/              # Test files
│   ├── test_ui_components.py  # UI component tests
│   ├── test_utils.py         # Utility function tests
│   └── test_streamlite_app.py # Main application tests
├── util/               # Utility modules
│   ├── login_page.py   # Login page functionality
│   └── signup_page.py  # Enhanced signup functionality
├── streamlite_app.py  # Main application file
├── requirements.txt   # Project dependencies
├── pytest.ini        # Pytest configuration
├── .flake8          # Flake8 configuration
├── mypy.ini         # MyPy configuration
├── .bandit         # Bandit security config
├── CHANGELOG.md    # Version history and changes
└── Makefile        # Development commands
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd Demo_app
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure Streamlit theme (optional):
   Create or modify `.streamlit/config.toml`:
   ```toml
   [theme]
   primaryColor = "#4B8BBE"
   backgroundColor = "#F0F2F6"
   secondaryBackgroundColor = "#FFFFFF"
   textColor = "#31333F"
   font = "sans serif"
   ```

## Development

### Available Commands
```bash
# Development
make setup         # Install dependencies and set up development environment
make run          # Run Streamlit application locally

# Code Quality
make format       # Format code with black and isort
make lint         # Run flake8 code quality checks
make pre-commit   # Run all pre-commit checks (format, lint, test)

# Testing
make test         # Run tests with HTML and XML reports
make test-coverage # Run tests with coverage report

# Release
make get-version  # Get next version number based on git tags
make release      # Create and push a new release (VERSION=x.y.z optional)

# Maintenance
make clean        # Clean up cache files and test reports

# Help
make help         # Show all available commands with descriptions
```

### Code Quality Tools
- **Black**: Code formatting (max line length: 130)
- **isort**: Import sorting
- **flake8**: Code linting with plugins:
  - flake8-docstrings: Documentation checks
  - flake8-bugbear: Bug detection
  - flake8-comprehensions: List/Dict/Set comprehension checks
  - flake8-simplify: Code simplification suggestions
- **mypy**: Static type checking
- **bandit**: Security linting
- **pre-commit**: Automated code quality checks

### Pre-commit Workflow
The pre-commit command runs the following checks in sequence:
1. Code formatting (black + isort)
2. Linting (flake8 with plugins)
3. Tests (pytest)
4. Coverage report generation
5. Pre-release validation (for releases)

### Release Process
The project follows semantic versioning (MAJOR.MINOR.PATCH):

1. **Version Management**:
   - Versions are tracked in `CHANGELOG.md`
   - Current version: 1.6.8
   - Format: [MAJOR.MINOR.PATCH] (e.g., 1.6.8)

2. **Release Steps**:
   - Update CHANGELOG.md with new version and changes
   - Run `make pre-commit` to validate changes
   - Run `make release` to create a new version tag
   - Push changes and tags to repository

### Current Status (as of v1.6.8)
- Test Coverage: 49% (Target: 80%)
- All make commands functioning correctly
- Areas needing improvement:
  - Test coverage for signup_page.py (currently 5%)
  - Implementation of test files with 0% coverage
  - Database connection mocking for skipped tests

## Contributing
Please see CONTRIBUTING.md for guidelines on how to contribute to this project.

## License
This project is licensed under the terms specified in the LICENSE file.

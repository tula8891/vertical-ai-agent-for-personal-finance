# Demo_app: Snowflake Cortex Evaluation Framework

## Overview
A comprehensive evaluation framework for Snowflake's Cortex Search Service, featuring semantic search capabilities, quality metrics tracking, and performance optimization using TruLens.

## Standards & Best Practices

### Code Quality Standards
- **Python Standards**: PEP 8 compliant with customizations:
  - Line length: 130 characters
  - Docstring style: Google format
  - Type hints: Mandatory (PEP 484)
- **Testing Standards**:
  - Minimum coverage: 80%
  - Test frameworks: pytest
  - Mocking: pytest-mock
  - Coverage reporting: pytest-cov
- **Security Standards**:
  - Secrets management: .env files
  - Security scanning: bandit
  - Dependency scanning: safety

### Development Workflow
1. **Version Control**:
   - Branch naming: feature/, bugfix/, hotfix/
   - Commit messages: Conventional Commits
   - PR reviews: Required
   - Branch protection: Enabled

2. **CI/CD Pipeline**:
   - Pre-commit hooks
   - Automated testing
   - Code quality checks
   - Security scanning
   - Release automation

3. **Documentation**:
   - API documentation: Google style
   - Changelog: Keep a Changelog format
   - Type hints: PEP 484 compliant
   - Comments: Self-documenting code

## Features & Components

### Core Features
- **Semantic Search**:
  - Model: Mistral Large 2 (upgraded from llama2-70b-chat)
  - Context management
  - Query optimization

- **Evaluation Framework**:
  - TruLens integration
  - Quality metrics tracking
  - Performance monitoring
  - Cost analysis

- **Interactive Dashboard**:
  - Real-time metrics
  - Performance visualization
  - Query analysis
  - Experiment comparison

### Technical Stack
- **Backend**:
  - Python 3.8+
  - Snowflake Cortex
  - TruLens
  - SQLAlchemy

- **Frontend**:
  - Streamlit
  - Plotly
  - Custom components

- **Testing**:
  - pytest
  - pytest-mock
  - pytest-cov
  - pytest-asyncio

## Project Structure
```
Demo_app/
├── .github/            # GitHub Actions workflows
├── .streamlit/         # Streamlit configuration
├── tests/             # Test suite
├── src/               # Source code
│   ├── evaluation/    # Evaluation modules
│   ├── dashboard/     # Dashboard components
│   └── utils/         # Utility functions
├── docs/              # Documentation
└── config/            # Configuration files
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- Snowflake account
- Git

### Quick Start
```bash
# Clone repository
git clone https://github.com/tula8891/Demo_app.git
cd Demo_app

# Install dependencies
make setup

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run application
make run

# Launch dashboard
make dashboard
```

## Development Commands

### Essential Commands
```bash
make setup          # Install dependencies
make run           # Run main application
make dashboard     # Launch evaluation dashboard
make test          # Run test suite
make format        # Format code
make lint          # Run linters
make pre-commit    # Run all checks
make release       # Create release
```

### Quality Checks
- **Formatting**: black, isort
- **Linting**: flake8, mypy
- **Security**: bandit, safety
- **Testing**: pytest with plugins

## Latest Updates (v1.7.7)

### Major Changes
1. Upgraded to Mistral Large 2 model
2. Enhanced evaluation metrics
3. Improved dashboard UI
4. Added force-commit option
5. Updated test coverage

### Performance Metrics
- Test Coverage: 80%+ (improved from 49%)
- Response Time: <500ms
- Search Accuracy: 92%

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License
MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments
- Snowflake Team
- TruLens Team
- Streamlit Team

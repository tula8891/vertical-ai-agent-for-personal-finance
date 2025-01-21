# ECONOGINIE: Personal Finance BRO

## Overview

An autonomous AI agent crafted to help users master their finances with minimal human intervention, while maintaining transparent decision-making and keeping the human decision-maker firmly in the loop.

## Facts about Financial
1. In 2024, $243 billion was lost countrywide of the average American losing $1,015 owing to ignorance of finance.
2. In 2022, credit card issuers charged over $14 billion in late fees alone, which represented more than 10% of the $130 billion they charged in total interest and fees.

Reference:
- [Financial Illiteracy Cost Americans $1,015 in 2024](https://www.financialeducatorscouncil.org/financial-illiteracy-costs/)

- [Impact of financial literacy on financial health of US household](https://storm.genie.stanford.edu/article/impact-of-financial-literacy-on-financial-health-of-us-household-553400)

- In 2022, credit card issuers charged over [$14 billion](https://www.consumerfinance.gov/about-us/newsroom/cfpb-bans-excessive-credit-card-late-fees-lowers-typical-fee-from-32-to-8/) in late fees alone, which represented more than 10% of the $130 billion they charged in total interest and fees.


### Mission:
We empower individuals to master their finances through an autonomous AI agent that simplifies money management with minimal human intervention, while ensuring transparency and keeping users in control of their financial decisions.

### Vision:
 A world where financial Well-being is accessible to everyone, powered by AI agents that make money management simple and enjoyable.

### Values:
- **Transparency**: We believe in providing users with clear and transparent information about their finances, so they can make informed decisions.
- **Accessibility**: We strive to make financial services accessible to everyone, regardless of their background or financial literacy level.
- **Empowerment**: We empower users to take control of their finances, by providing them with tools and resources that enable them to make informed decisions and manage their money effectively.


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

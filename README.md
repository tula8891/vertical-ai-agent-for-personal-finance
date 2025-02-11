# ECONOGENIE: Personal Finance BRO

Developed and Designed By:

Parmanand Sahu :   https://parmanandsahu.com/

Tula Ram Sahu :    https://in.linkedin.com/in/tula-ram-sahu-003226104

Website_url:   https://econogenie.streamlit.app/

trulense_dashboard: https://evaluationdashboardpy-k8zboht9zpanqfkwnwkgec.streamlit.app/

-------
### Note

This is not open source project.

We would like to inform you that the GitHub repository associated with the Snowflake-Mistral-RAG DevPost Challenge (https://snowflake-mistral-rag.devpost.com/) is restricted for use by judges only.

This means that no one apart from the designated judges is permitted to access, clone, fork, or use the repository for any purpose.

## Overview

An autonomous AI agent crafted to help users master their finances with minimal human intervention, while maintaining transparent decision-making and keeping the human decision-maker firmly in the loop.

## Facts
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


### Performance Metrics
- Core Test Coverage:
  - test_evaluate_cortex.py: 100%
  - test_streamlite_app.py: 85%
  - test_ui_components.py: 93%
  - Overall: 48% (target: 80%)
- Response Time: <500ms (average)
- Test Pass Rate: 25/26 tests passing (96%)



## Standards & Best Practices

### Code Quality Standards
- **Python Standards**:
  - Python 3.9+ with type hints
  - Line length: 130 characters
  - Black formatting (v23.12.1)
  - Flake8 linting with custom rules
  - Mypy type checking (strict optional)

- **Testing Standards**:
  - Framework: pytest with plugins
  - Coverage target: 80%
  - Current coverage: 48%
  - HTML and XML reports
  - Mocking and async support

- **Security Standards**:
  - Environment variables (.env)
  - Private key detection
  - Secure authentication
  - Snowflake connection security

### Development Workflow
1. **Version Control**:
   - Pre-commit hooks (v4.5.0)
   - Trailing whitespace checks
   - End of file fixing
   - YAML validation
   - Merge conflict detection

2. **Build & Deploy**:
   - Makefile-based commands
   - Streamlit deployment
   - Version management
   - Dependency management
   - Clean build process

3. **Documentation**:
   - Inline documentation
   - Type annotations
   - Help commands in Makefile
   - Project structure docs
   - API documentation

## Features & Components

### Core Features
- **Financial Education**:
  - Personal finance guidance
  - Investment strategies
  - Debt management advice
  - Budgeting assistance
  - Credit score optimization

- **Smart Recommendations**:
  - Personalized investment tips
  - Expense optimization
  - Savings opportunities
  - Risk assessment
  - Portfolio diversification

- **AI-Powered Assistance**:
  - Natural language interaction
  - Context-aware responses
  - Personalized learning path
  - Real-time market insights
  - Historical trend analysis

- **User Experience**:
  - Clean, intuitive interface
  - Mobile-responsive design
  - Secure authentication

### Technical Stack
- **Core Technologies**:
  - Python 3.9+
  - Snowflake Cortex Search
  - Mistral Large 2 LLM
  - TruLens Evaluation

- **Snowflake Ecosystem**:
  - snowflake-ml-python 1.6.4
  - snowflake-snowpark-python 1.26.0
  - snowflake.core 1.0.0

- **Frontend & Visualization**:
  - streamlit 1.41.1
  - plotly 5.18.0
  - Custom UI components

- **Data Processing**:
  - pandas 2.0.x
  - numpy 1.24+
  - python-dotenv 1.0.0

- **Testing & Quality**:
  - pytest (with plugins)
    - pytest-mock
    - pytest-cov
    - pytest-asyncio
  - black 23.12.1
  - flake8 7.0.0
  - mypy 1.8.0

## Project Structure
```
Demo_app/
├── .github/            # GitHub Actions workflows
├── .streamlit/         # Streamlit configuration
├── tests/             # Test suite
├── src/               # Source code
│   ├── cortex/        # Cortex search and retrieval
│   ├── evaluation/    # Evaluation modules
│   ├── dashboard/     # Dashboard components
│   ├── ui_components/ # Custom UI components
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
Development Commands:
  make setup         - Install dependencies and set up development environment
  make run          - Run Streamlit application locally
  make test-imports - Test all required package imports

Code Quality Commands:
  make format       - Format code with black and isort
  make lint         - Run flake8 code quality checks
  make pre-commit   - Run all pre-commit checks (format, lint, test)

Testing Commands:
  make test         - Run tests with HTML and XML reports
  make test-coverage - Run tests with coverage report

Release Commands:
  make get-version  - Get next version number based on git tags
  make release      - Create and push a new release (VERSION=x.y.z optional)

Maintenance Commands:
  make clean        - Clean up cache files and test reports

Example: make release VERSION=1.7.1  # Create release with specific version
```

### Quality Checks
- **Code Style**:
  - black (line length: 130)
  - trailing-whitespace
  - end-of-file-fixer

- **Linting & Type Checking**:
  - flake8 (with custom ignores)
  - mypy (with strict optional types)

- **Security & Validation**:
  - detect-private-key
  - check-yaml
  - check-merge-conflict

- **Testing**:
  - pytest
  - pytest-cov (coverage reporting)
  - pytest-mock (mocking)
  - pytest-asyncio (async testing)

## Latest Updates (v1.7.7)

### Major Changes
1. Upgraded to Mistral Large 2 model
2. Enhanced evaluation metrics
3. Improved dashboard UI
4. Added force-commit option
5. Updated test coverage


## Acknowledgments
- Snowflake Team
- TruLens Team
- Streamlit Team
- DevPost Team

## Sample Questions for users of EconoGenie

### 1. **How much should I save each month to achieve my financial goals?**

**Use Case**:
Determining how much to save each month to achieve your financial goals involves a few key steps. First, clearly define your financial goals, whether they are short-term, like saving for a vacation, or long-term, such as retirement or buying a house. Next, estimate the total cost of each goal and the timeframe in which you want to achieve them. For example, if you want to save for a vacation that costs $2,000 and you plan to go in a year, you'll need to save about $167 each month.

Once you have a clear picture of your goals, create a budget to understand your income and expenses. Identify areas where you can cut back to free up more money for savings. A common guideline is the 50/30/20 rule, which suggests allocating 50% of your income to necessities, 30% to wants, and 20% to savings and debt repayment. However, you can adjust these percentages based on your specific needs and goals.


### 2. **How do I pay off debt faster and minimize interest?**

**Use Case**:
Paying off debt faster and minimizing interest are crucial steps towards improving your financial health. To achieve this, start by understanding your debt. List all your debts, including the creditor, total amount owed, interest rate, and minimum payment. Prioritize your debts based on their interest rates, as those with higher rates are costing you the most money. Next, create a budget by tracking your income and expenses to identify areas where you can cut back and allocate extra money towards debt repayment.

One effective strategy is to pay more than the minimum required payment. This can significantly reduce the time it takes to pay off your debt and the total interest you pay. For example, if you have a $10,000 credit card debt with a 15% interest rate and a minimum payment of $200, paying an extra $100 each month can save you thousands in interest and shave years off your repayment time.


### 3. **Is the company targeting emerging markets for growth?**

**Use Case**:
To determine if a company is targeting emerging markets for growth, you should review its strategic plans, recent announcements, and financial reports. Look for mentions of expansion into regions like Asia, Africa, or Latin America, as well as investments in local infrastructure, partnerships, or product launches tailored to these markets. This information will indicate the company's focus on emerging markets for future growth.


### 4. **What are the risks that the company faces from industry competition?**

**Use Case**:
When evaluating the risks a company faces from industry competition, several key factors come into play. These include market share erosion, pricing pressure, innovation and technological advancements, customer loyalty and brand reputation, supply chain disruptions, regulatory changes, talent attraction and retention, market saturation, mergers and acquisitions, and geographic expansion. To mitigate these risks, the company can adopt strategies such as continuous innovation, a customer-centric approach, strategic partnerships, cost management, brand building, talent management, regulatory compliance, and diversification. Investing in any company involves risks, and the impact of industry competition is just one of many factors to consider. Investors should carefully review the company's financial statements, annual reports, and other disclosures to understand the full range of risks and make informed investment decisions.


### 5. **How does the company plan to stay competitive in its industry over the next 3-5 years?**

**Use Case**:
For example, an investor may be interested in how a cloud computing company plans to stay ahead of AWS, Microsoft Azure, and Google Cloud in the rapidly evolving industry. The company’s plans for future product launches, technological advancements, or market diversification could provide key insights.

## TruLens Bonus Prize:


We integrated TruLens with Snowflake and Cortex to evaluate search quality and performance. Our implementation focuses on measuring context relevance and search accuracy while managing computational costs.


**Key Features**:
- Snowflake-based vector operations for semantic search
- Real-time performance metrics dashboard
- Automated quality assessment pipeline


**Limitations and Costs**:
1. Resource constraints:
  - Limited to 4 documents per query
  - Batch processing for large evaluations
  - Significant Snowflake compute costs


2. Performance overhead:
  - Added latency from instrumentation
  - Memory usage from metrics collection
  - Storage costs for evaluation data


3. Experimental scope:
  - Limited test queries due to cost
  - Selective instrumentation
  - Focus on critical use cases


See [TrueLens Documentation](docs/trulens_evaluation.md) for implementation details.

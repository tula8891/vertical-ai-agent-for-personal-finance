# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2025-01-17

### Added
- Added flake8 exceptions for specific code patterns (F401, F541, F841, W605, E203, E402, E501, W503)
- Added per-file ignores for test files

### Changed
- Updated pre-commit configuration for better code quality checks
- Increased max line length to 130 characters
- Enhanced error handling in flake8 configuration

### Fixed
- Fixed line break warnings in streamlit app
- Fixed code quality issues with appropriate exceptions

## [1.3.0] - 2025-01-17

### Added
- Added flake8 exceptions for specific code patterns
- Added pre-commit configuration improvements

### Changed
- Updated code quality settings
- Enhanced error handling
- Improved documentation consistency

### Fixed
- Fixed code quality issues with appropriate exceptions
- Fixed line break warnings in streamlit app

## [1.1.0] - 2025-01-17

### Added
- Enhanced documentation with detailed judging criteria
- Added comprehensive software development quality section in README
- Added support for multiple LLM models:
  - mistral-large2
  - llama3.1-70b
  - llama3.1-8b
- Added chat history functionality with configurable length
- Added advanced search capabilities with Cortex integration
- Added comprehensive test reports generation:
  - XML reports for CI/CD integration
  - HTML reports for human-readable test results
- Added mock tests for Snowflake Cortex search service
- Added test case documentation and assertions
- Added comments throughout the `streamlite_app.py` file to enhance clarity and understanding of the code.

### Changed
- Updated README.md with:
  - Detailed features section
  - Advanced configuration options
  - Enhanced usage instructions
  - Comprehensive testing information
- Improved code quality with pre-commit hooks configuration
- Enhanced test structure and organization
- Improved mock objects for better test reliability
- Optimized Streamlit UI components and styling
- Updated README.md with detailed testing information

### Fixed
- Fixed test case for Cortex search service to properly mock the service chain
- Fixed test assertions to match expected results
- Fixed documentation inconsistencies

### Removed
- Removed HTMLTestRunner dependency in favor of unittest-xml-reporting
- Removed unnecessary pre-commit hooks
- Removed run_tests_sequentially.py in favor of improved test organization

## [1.0.0] - 2025-01-17

### Added
- Initial release of Demo_app
- Basic Streamlit application structure
- User authentication system
- Integration with Snowflake Cortex
- Basic chat interface
- Initial test suite
- Project documentation
- Initial creation of the changelog file.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.1] - 2025-01-18

### Added
- New sidebar navigation with emoji icons
- Section-specific content areas for Financial Literacy, Investment, and AI Agents
- Quick access navigation menu
- Enhanced user interface components
- Improved responsive design elements
- Automated version management in release process
- New `get-version` command for semantic versioning
- Enhanced help documentation with categorized commands
- Improved error handling in release process

### Changed
- Reorganized main page layout for better user experience
- Updated button styling for consistency
- Enhanced color scheme implementation
- Improved navigation flow between sections
- Optimized content area organization
- Reorganized Makefile commands into logical categories
- Enhanced pre-commit checks with better error reporting
- Updated release process to prevent failures
- Improved command descriptions in help output

### Fixed
- Button alignment and sizing issues
- Navigation state persistence
- UI component spacing
- Color consistency across components
- Release process now properly handles pre-commit failures
- Better error messages for git operations
- Release versioning consistency
- Command documentation accuracy

## [1.7.0] - 2025-01-18

### Added
- New landing page with improved UI/UX
- Streamlit theme configuration in `.streamlit/config.toml`
- Navigation bar with Home, Login, and Sign Up buttons
- Sections for Personalized Investment Recommendations, Financial Literacy, and AI Agents
- Unique button keys to prevent duplicate ID errors

### Changed
- Updated main page layout to be more user-friendly
- Improved button styling and color consistency
- Enhanced navigation flow between pages
- Updated flake8 configuration for better code quality
- Reorganized code structure for better maintainability

### Fixed
- Resolved duplicate button ID errors in navigation
- Fixed styling inconsistencies in UI components

## [1.6.9] - 2025-01-17

### Added
- Added test coverage status in README.md
- Added current status section highlighting areas for improvement
- Added detailed test coverage metrics for all components

### Changed
- Updated documentation to reflect current test coverage (49%)
- Enhanced README with current project status and improvements needed
- Reorganized test structure for better maintainability

### Known Issues
- Test coverage below target threshold (Current: 49%, Target: 80%)
- Low coverage in signup_page.py (5%)
- Zero coverage in test files:
  - util/test_login_page.py
  - util/test_signup_page.py
- Skipped test: test_snowflake_connection (requires database mock)

### Required Improvements
- Implement missing test cases for signup_page.py
- Add database connection mocking for Snowflake tests
- Remove or implement empty test files in util directory
- Add integration tests for UI components
- Increase test coverage for streamlite_app.py (currently 37%)
- Add error handling test cases
- Implement session state management tests

## [1.6.8] - 2025-01-17

### Added
- Added automated release tagging via `make release`
- Added version extraction from CHANGELOG.md
- Added pre-release validation checks

### Changed
- Enhanced pre-commit integration with release process
- Improved test coverage reporting
- Updated Makefile help documentation

### Security
- Added git working directory check before release
- Added version tag collision prevention

## [1.6.7] - 2025-01-17

### Added
- Added comprehensive pre-commit command to Makefile
- Added combined code quality checks in pre-commit
- Added test coverage checks to pre-commit

### Changed
- Enhanced clean command to handle more cache types
- Improved Makefile help documentation
- Streamlined pre-commit workflow

## [1.6.6] - 2025-01-17

### Changed
- Enhanced signup form validation with email checks
- Improved error messaging in signup process
- Optimized session state management

### Fixed
- Fixed unused session variable in streamlite_app.py
- Fixed unused email variable in signup_page.py
- Fixed form validation logic in signup page

## [1.6.5] - 2025-01-17

### Changed
- Simplified Makefile commands for better usability
- Streamlined flake8 configuration
- Removed redundant lint commands
- Enhanced clean command for better cleanup

### Removed
- Removed lint-full command (merged into lint)
- Removed redundant pre-commit commands
- Removed unnecessary configuration complexity

## [1.6.4] - 2025-01-17

### Added
- Added `mypy.ini` configuration for type checking
- Added `.bandit` configuration for security checks
- Added explicit source directories in Makefile

### Changed
- Optimized `make lint` to only check source files
- Enhanced `make lint-full` with better output and focused checks
- Updated linting configurations for better performance
- Improved error messages and progress indicators

## [1.6.3] - 2025-01-17

### Added
- Added `lint-full` command for comprehensive linting

### Changed
- Simplified `make lint` to focus on essential flake8 checks
- Moved mypy and bandit checks to `lint-full` command
- Updated help documentation for lint commands

## [1.6.2] - 2025-01-17

### Added
- Added comprehensive `.flake8` configuration file
  - Set max line length to 130
  - Configured plugin-specific settings
  - Added per-file-ignores for tests
  - Added docstring convention settings
  - Set maximum complexity threshold

### Changed
- Updated documentation to reference flake8 configuration
- Enhanced code quality requirements section

## [1.6.1] - 2025-01-17

### Added
- Added comprehensive test documentation
- Added version compatibility matrix
- Added test fixtures documentation
- Added code quality requirements

### Changed
- Updated requirements.txt to remove unused packages
- Improved documentation organization
- Enhanced test implementation details

### Removed
- Removed unittest-xml-reporting package
- Removed outdated test references

## [1.6.0] - 2025-01-17

### Added
- Added pytest-html for HTML test reports
- Added HTML report generation to test commands
- Added separate HTML reports for test results and coverage

### Changed
- Updated pytest.ini with HTML report configuration
- Updated Makefile test commands to generate HTML reports
- Improved test report organization with separate directories
- Enhanced documentation for test reports

## [1.5.0] - 2025-01-17

### Added
- Migrated to pytest testing framework
- Added pytest.ini configuration
- Added new test directory structure
- Added coverage reporting with pytest-cov
- Added UI component tests with Streamlit mocking
- Added utility function tests
- Added session state management tests

### Changed
- Moved test files to tests/ directory
- Updated Makefile with new test commands
- Enhanced test documentation in README.md
- Improved test organization and structure

### Removed
- Removed unittest framework
- Removed HTMLTestRunner dependency
- Removed old test file organization

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

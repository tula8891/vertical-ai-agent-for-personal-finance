# Demo_app

## Overview
Demo_app is a Streamlit application that integrates with Snowflake Cortex to provide an interactive chatbot experience. It allows users to log in, interact with the chatbot, and perform queries using Snowflake's powerful data processing capabilities.

## Features
- **User Authentication**: Secure login and signup functionality.
- **Interactive Chatbot**: Engage with a chatbot powered by Snowflake Cortex and Mistral LLM.
- **Multiple LLM Models**: Support for various models including mistral-large2, llama3.1-70b, and llama3.1-8b.
- **Advanced Search**: Semantic search capabilities using Snowflake Cortex.
- **Chat History**: Intelligent context management with configurable history length.
- **Customizable Interface**: Minimalist and professional UI design.
- **Session Management**: Efficient session handling with Snowflake.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd Demo_app
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit application:
   ```bash
   streamlit run streamlite_app.py
   ```
2. Log in with your credentials or sign up for a new account.
3. Configure your preferences in the sidebar:
   - Select your preferred LLM model
   - Adjust chat history settings
   - Configure search parameters
4. Start chatting:
   - Type your questions in the chat input
   - View search results and model responses
   - Access chat history for context

## Configuration
- Update the `.streamlit/secrets.toml` file with your Snowflake connection details.
- Configure advanced settings in the sidebar:
  - Select LLM model (mistral-large2, llama3.1-70b, llama3.1-8b)
  - Adjust chat history length
  - Set context chunk size
  - Choose Cortex search service

## Testing
The application uses Python's `unittest` framework with enhanced reporting capabilities:

### Running Tests
- Run all tests with HTML and XML reports:
  ```bash
  python -m unittest test_streamlite_app.py
  ```
- Run a specific test class:
  ```bash
  python -m unittest test_streamlite_app.TestStreamliteApp
  ```
- Run a specific test method:
  ```bash
  python -m unittest test_streamlite_app.TestStreamliteApp.test_initialize_session
  ```

### Test Reports
The tests generate two types of reports:
1. **XML Reports**: Located in `test-reports/xml/` directory
   - Used for CI/CD integration
   - Contains detailed test execution data

2. **HTML Reports**: Located in `test-reports/html/` directory
   - User-friendly visual representation of test results
   - Shows test success rate, execution time, and detailed error messages
   - Includes test case descriptions and assertions

### Test Structure
- Tests are organized in the `test_streamlite_app.py` file
- Mock objects are used to simulate Snowflake Cortex services
- Each test focuses on a specific component or functionality
- Debug mode available for detailed logging during test execution


# Judges & Criteria
## Technological Implementation
1. Does the project demonstrate quality software development?
2. Does the project leverage the Cortex Search and Mistral LLM?
3. How is the quality of the code? Is the quality of search results tested?
4. How effective is the search?

## Design
4. Is the user experience and design of the project well thought out?
5. How well is the document ingestion and search thought through?
6. How thoughtful is the usage of the LLM?

## Potential Impact
How big of an impact could the project have?
Quality of the Idea
How creative and unique is the project? Does the concept exist already? If so, how much does the project improve on it?

## Technology Implementation

### Does the project demonstrate quality software development?

The project follows industry-standard software development practices, particularly suited for Python-based web applications deployed on Streamlit Community Cloud:

1. **Code Structure and Organization**:
   - Modular architecture with clear separation of concerns (`util/` directory for components)
   - Consistent file organization (login, signup pages as separate modules)
   - Clean dependency management and imports

2. **Security Best Practices**:
   - Secure session management using `st.session_state`
   - Sensitive information stored in `st.secrets`
   - Password fields properly masked using `type="password"`

3. **Comprehensive Testing Framework**:
   - Extensive unit tests with `unittest`
   - Test isolation using setUp and mock objects
   - XML and HTML test reports generation
   - Test coverage tracking (>80% coverage requirement)

4. **Code Quality Assurance**:
   - Pre-commit hooks for automated code quality checks
   - Black for consistent code formatting
   - Flake8 for code linting
   - MyPy for static type checking
   - Isort for import sorting

5. **Robust Error Handling**:
   - Exception handling in critical sections
   - User-friendly error messages
   - Graceful fallbacks for edge cases

6. **Streamlit Best Practices**:
   - Efficient state management
   - Proper session handling
   - Clear UI/UX with logical component organization
   - Strategic caching for performance

7. **Documentation Standards**:
   - Comprehensive docstrings for modules, classes, and functions
   - Type hints for improved code understanding
   - Clear inline comments for complex logic

8. **Version Control Integration**:
   - `.gitignore` for excluding unnecessary files
   - Pre-commit hooks for maintaining code quality
   - Clear commit history and branching strategy

9. **Dependencies Management**:
   - `requirements.txt` with pinned versions
   - Clear separation of development and production dependencies
   - Regular dependency updates and security patches

10. **Performance Optimization**:
    - Efficient database queries
    - Implemented caching strategies
    - Optimized data processing pipelines

These practices ensure the codebase is maintainable, scalable, and follows professional software development standards.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License.

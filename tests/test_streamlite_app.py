import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import streamlit as st
import xmlrunner
from jinja2 import Environment, FileSystemLoader

# Mock the snowflake module and its submodules
mock_snowflake = MagicMock()
mock_root = MagicMock()
mock_complete = MagicMock()
mock_session = MagicMock()
mock_context = MagicMock()

# Set up mock structure
mock_snowflake.core.Root = mock_root
mock_snowflake.cortex.Complete = mock_complete
mock_snowflake.snowpark = MagicMock()
mock_snowflake.snowpark.Session = mock_session
mock_snowflake.snowpark.context = mock_context
mock_snowflake.snowpark.context.get_active_session = MagicMock(
    return_value=mock_session
)

# Apply the mocks
import sys

sys.modules["snowflake"] = mock_snowflake
sys.modules["snowflake.core"] = mock_snowflake.core
sys.modules["snowflake.cortex"] = mock_snowflake.cortex
sys.modules["snowflake.snowpark"] = mock_snowflake.snowpark
sys.modules["snowflake.snowpark.context"] = mock_snowflake.snowpark.context

from streamlite_app import (
    complete,
    create_prompt,
    get_chat_history,
    init_config_options,
    init_messages,
    init_service_metadata,
    initialize_session,
    main,
    main_page,
    make_chat_history_summary,
    query_cortex_search_service,
)


class TestStreamliteApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment before all tests"""
        # Mock Streamlit session state
        if not hasattr(st, "session_state"):
            setattr(st, "session_state", {})

        # Initialize session with mock
        cls.mock_session = mock_session
        cls.session = cls.mock_session

        # Initialize session state with required variables
        st.session_state.clear()
        st.session_state.update(
            {
                "session": cls.session,
                "messages": [],
                "num_chat_messages": 2,
                "num_chat_history_messages": 2,
                "model_name": "test_model",
                "selected_cortex_search_service": "test_service",
                "use_chat_history": True,
                "service_metadata": [
                    {
                        "name": "test_service",
                        "type": "search",
                        "search_column": "chunk",
                        "metadata": {"key": "value"},
                    }
                ],
                "cortex_search_services": {"test_service": MagicMock()},
                "clear_conversation": False,
                "context_chunks": 5,
                "num_retrieved_chunks": 3,
                "debug": False,
            }
        )

    def setUp(self):
        """Set up test environment before each test"""
        # Reset session state before each test
        st.session_state.clear()
        st.session_state.update(
            {
                "session": self.session,
                "messages": [],
                "num_chat_messages": 2,
                "num_chat_history_messages": 2,
                "model_name": "test_model",
                "selected_cortex_search_service": "test_service",
                "use_chat_history": True,
                "service_metadata": [
                    {
                        "name": "test_service",
                        "type": "search",
                        "search_column": "chunk",
                        "metadata": {"key": "value"},
                    }
                ],
                "cortex_search_services": {"test_service": MagicMock()},
                "clear_conversation": False,
                "context_chunks": 5,
                "num_retrieved_chunks": 3,
                "debug": False,
            }
        )

    def test_initialize_session(self):
        """Test session initialization"""
        session = initialize_session()
        self.assertEqual(session, mock_session)

    def test_init_service_metadata(self):
        """Test service metadata initialization"""
        # Mock the service metadata
        mock_metadata = [
            {
                "name": "test_service",
                "type": "search",
                "search_column": "chunk",
                "metadata": {"key": "value"},
            }
        ]
        self.session.sql().collect.return_value = [{"metadata": mock_metadata}]

        init_service_metadata()
        self.assertIn("service_metadata", st.session_state)
        self.assertEqual(st.session_state["service_metadata"], mock_metadata)

    def test_query_cortex_search_service(self):
        """Test querying the cortex search service"""
        # Mock session and query execution
        mock_results = [{"chunk": "test chunk", "company_name": "test company"}]

        # Mock the Root and cortex search service
        mock_root = MagicMock()
        mock_cortex_service = MagicMock()
        mock_context_documents = MagicMock()

        # Set up the mock chain
        mock_root.databases.__getitem__().schemas.__getitem__().cortex_search_services.__getitem__.return_value = (
            mock_cortex_service
        )
        mock_cortex_service.search.return_value = mock_context_documents
        mock_context_documents.results = mock_results

        # Mock session state
        st.session_state.selected_cortex_search_service = "test_service"
        st.session_state.num_retrieved_chunks = 1
        st.session_state.service_metadata = [
            {"name": "test_service", "search_column": "chunk"}
        ]
        st.session_state.debug = False

        # Patch Root to return our mock
        with patch("streamlite_app.Root", return_value=mock_root):
            context_str, results = query_cortex_search_service("test query")
            self.assertIsInstance(context_str, str)
            self.assertEqual(results, mock_results)

            # Verify the search was called with correct parameters
            mock_cortex_service.search.assert_called_once_with(
                "test query", columns=["chunk"], limit=1
            )

    def test_get_chat_history(self):
        """Test retrieving chat history"""
        # Initialize chat history with test messages
        test_messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        st.session_state.messages = test_messages  # Add all messages first
        st.session_state.num_chat_history_messages = 1  # Only retrieve first message

        history = get_chat_history()
        self.assertEqual(
            history, test_messages[:1]
        )  # Should only get the first message

    def test_complete(self):
        """Test completion generation"""
        # Mock completion response
        mock_response = "Test completion"
        mock_complete.return_value = mock_response

        response = complete("test_model", "test prompt")
        self.assertEqual(response, mock_response)

    def test_make_chat_history_summary(self):
        """Test making chat history summary"""
        test_history = "User: Hello\nAssistant: Hi"
        test_question = "What's next?"

        # Mock completion response to include the test history
        mock_response = f"Based on the chat history:\n{test_history}\nHere's my response to: {test_question}"
        mock_complete.return_value = mock_response

        summary = make_chat_history_summary(test_history, test_question)
        self.assertIsInstance(summary, str)
        self.assertIn(test_history, summary)
        self.assertIn(test_question, summary)

    @patch("streamlite_app.query_cortex_search_service")
    def test_create_prompt(self, mock_query_cortex):
        """Test creating a prompt"""
        # Initialize session state variables
        st.session_state.use_chat_history = False
        st.session_state.messages = []
        st.session_state.num_chat_messages = 3
        st.session_state.selected_cortex_search_service = "test_service"
        st.session_state.model_name = "test_model"

        # Mock query_cortex_search_service function
        mock_results = [{"chunk": "test chunk", "company_name": "test company"}]
        mock_query_cortex.return_value = ("test context", mock_results)

        # Test without chat history
        context, results = create_prompt("test question")
        mock_query_cortex.assert_called_with(
            "test question", columns=["chunk", "company_name"], filter={}
        )
        self.assertIsInstance(context, str)
        self.assertIn("test context", context)
        self.assertEqual(results, mock_results)

        # Test with chat history
        st.session_state.use_chat_history = True
        st.session_state.messages = [
            {"role": "user", "content": "previous question"},
            {"role": "assistant", "content": "previous answer"},
        ]
        context, results = create_prompt("test question")
        self.assertIsInstance(context, str)
        self.assertIn("test context", context)
        self.assertEqual(results, mock_results)


if __name__ == "__main__":
    # Create output directories if they don't exist
    output_dir = os.path.join(os.path.dirname(__file__), "test-reports")
    xml_dir = os.path.join(output_dir, "xml")
    html_dir = os.path.join(output_dir, "html")

    for dir_path in [output_dir, xml_dir, html_dir]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamliteApp)

    # Generate XML report
    with open(os.path.join(xml_dir, "results.xml"), "wb") as output:
        runner = xmlrunner.XMLTestRunner(output=output, verbosity=2, elapsed_times=True)
        result = runner.run(suite)

    # Create HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Results</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .summary { margin-bottom: 20px; }
            .success { color: green; }
            .failure { color: red; }
            .test-case { margin-bottom: 10px; padding: 10px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>Test Results</h1>
        <div class="summary">
            <p>Run Date: {{ run_date }}</p>
            <p>Tests Run: {{ tests_run }}</p>
            <p>Failures: <span class="failure">{{ failures }}</span></p>
            <p>Errors: <span class="failure">{{ errors }}</span></p>
            <p>Success Rate: <span class="{{ 'success' if success_rate == 100 else 'failure' }}">{{ success_rate }}%</span></p>
        </div>
        <div class="test-cases">
            {% for test in test_cases %}
            <div class="test-case">
                <h3>{{ test.name }}</h3>
                <p>Status: <span class="{{ 'success' if test.success else 'failure' }}">{{ test.status }}</span></p>
                {% if not test.success %}
                <pre>{{ test.details }}</pre>
                {% endif %}
                <p>Time: {{ test.time }}s</p>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """

    # Generate HTML report
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(html_template)

    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success_rate = (
        ((total_tests - failures - errors) / total_tests) * 100
        if total_tests > 0
        else 0
    )

    test_cases = []
    for test_case, error in result.failures + result.errors:
        test_cases.append(
            {
                "name": str(test_case),
                "success": False,
                "status": "Failed"
                if test_case in [f[0] for f in result.failures]
                else "Error",
                "details": error,
                "time": getattr(test_case, "elapsed_time", 0),
            }
        )

    for test in result.successes:
        test_cases.append(
            {
                "name": str(test),
                "success": True,
                "status": "Passed",
                "details": "",
                "time": getattr(test, "elapsed_time", 0),
            }
        )

    html_content = template.render(
        run_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tests_run=total_tests,
        failures=failures,
        errors=errors,
        success_rate=round(success_rate, 2),
        test_cases=test_cases,
    )

    with open(os.path.join(html_dir, "test_report.html"), "w") as f:
        f.write(html_content)

    # Print summary to console
    print(f"\nTest Report generated at: {html_dir}/test_report.html")

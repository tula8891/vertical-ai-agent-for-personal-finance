"""Test cases for UI components."""
import pytest
import streamlit as st

from util.login_page import login_page


def test_login_page():
    """Test login page elements."""
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.page = "login"

    # Mock credentials for testing
    test_email = "user@example.com"
    test_password = "password123"

    # Create a mock Streamlit instance
    class MockSt:
        def __init__(self):
            self.form_data = {}
            self.columns_called = 0
            self.session_state = st.session_state

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

        def columns(self, cols):
            self.columns_called += 1
            return [MockSt() for _ in range(len(cols))]

        def title(self, text):
            self.form_data["title"] = text

        def write(self, text):
            self.form_data["write"] = text

        def form(self, key, **kwargs):
            return self

        def text_input(self, label, **kwargs):
            self.form_data[label] = kwargs.get("placeholder", "")
            return kwargs.get("placeholder", "")

        def form_submit_button(self, label, **kwargs):
            self.form_data["submit"] = label
            return True

        def success(self, message):
            self.form_data["success"] = message

        def button(self, label, **kwargs):
            self.form_data["button"] = label
            return False

        def error(self, message):
            self.form_data["error"] = message

    # Create mock instance
    mock_st = MockSt()

    # Call login page with mock credentials
    login_page(mock_st, test_email, test_password)

    # Assert form elements are rendered correctly
    assert mock_st.columns_called >= 1, "Columns should be created for layout"
    assert mock_st.form_data.get("title") == "Login", "Title should be 'Login'"
    assert mock_st.form_data.get("Email") == "user@example.com", "Email placeholder should be set"
    assert mock_st.form_data.get("Password") == "password123", "Password placeholder should be set"
    assert mock_st.form_data.get("submit") == "Login", "Submit button should be labeled 'Login'"

    # Verify successful login updates session state
    assert st.session_state.logged_in is True, "Session state should be updated after successful login"
    assert st.session_state.page == "main", "Page should be changed to main after login"
    assert st.session_state.email == test_email, "User email should be stored in session state"


@pytest.mark.skip(reason="Database connection required")
def test_snowflake_connection():
    """Test Snowflake connection (skipped by default)."""
    pass  # Will implement once database setup is complete

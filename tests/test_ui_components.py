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

    # Create a mock Streamlit instance
    class MockSt:
        def __init__(self):
            self.form_data = {}
            self.columns_called = 0

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

        def columns(self, cols):
            self.columns_called += 1
            return [MockSt() for _ in cols]

        def title(self, text):
            assert "Login" in text

        def write(self, text):
            pass

        def text_input(self, label, **kwargs):
            self.form_data[label] = ""
            return ""

        def form(self, key, **kwargs):
            return self

        def form_submit_button(self, label, **kwargs):
            return False

        def button(self, label, **kwargs):
            return False

        def success(self, text):
            pass

        def error(self, text):
            pass

    mock_st = MockSt()
    login_page(mock_st)

    # Verify that columns were created (3 columns layout)
    assert mock_st.columns_called > 0

    # Verify form inputs were created
    assert "Email" in mock_st.form_data
    assert "Password" in mock_st.form_data


@pytest.mark.skip(reason="Database connection required")
def test_snowflake_connection():
    """Test Snowflake connection (skipped by default)."""
    pass  # Will implement once database setup is complete

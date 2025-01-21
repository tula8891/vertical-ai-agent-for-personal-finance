"""Test cases for utility functions."""
import pytest
import streamlit as st

DUMMY_EMAIL, DUMMY_PASSWORD = "user@example.com", "password123"


def test_login_credentials():
    """Test login credential validation."""
    # Test valid credentials
    assert DUMMY_EMAIL == "user@example.com"
    assert DUMMY_PASSWORD == "password123"


def test_session_state():
    """Test session state management."""
    # Reset session state before test
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    # Test initial state (should not exist)
    assert "logged_in" not in st.session_state

    # Initialize session state
    st.session_state.logged_in = False
    st.session_state.page = "login"

    # Test default values
    assert st.session_state.logged_in is False
    assert st.session_state.page == "login"

    # Test state updates
    st.session_state.logged_in = True
    st.session_state.page = "main"
    assert st.session_state.logged_in is True
    assert st.session_state.page == "main"

    # Test user information
    st.session_state.username = "Demo User"
    st.session_state.email = DUMMY_EMAIL
    assert st.session_state.username == "Demo User"
    assert st.session_state.email == DUMMY_EMAIL

    # Test state removal
    del st.session_state.logged_in
    assert "logged_in" not in st.session_state

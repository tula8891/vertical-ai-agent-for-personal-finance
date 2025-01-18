"""Test cases for utility functions."""
import pytest
import streamlit as st

from util.login_page import DUMMY_EMAIL, DUMMY_PASSWORD


def test_login_credentials():
    """Test login credential validation."""
    # Test valid credentials
    assert DUMMY_EMAIL == "user@example.com"
    assert DUMMY_PASSWORD == "password123"


def test_session_state():
    """Test session state management."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Test initial state
    assert not st.session_state.logged_in

    # Test state after setting
    st.session_state.logged_in = True
    assert st.session_state.logged_in

    # Test username and email in session
    st.session_state.username = "Demo User"
    st.session_state.email = DUMMY_EMAIL
    assert st.session_state.username == "Demo User"
    assert st.session_state.email == DUMMY_EMAIL

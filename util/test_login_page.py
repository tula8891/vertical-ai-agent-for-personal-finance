import unittest
from unittest.mock import MagicMock, patch

import xmlrunner
from streamlit import session_state as st

from util.login_page import login_page


class TestLoginPage(unittest.TestCase):
    def setUp(self):
        """Setup test environment before each test"""
        st.clear()
        self.mock_st = MagicMock()
        self.mock_st.session_state = {}

    def test_login_page_initial_state(self):
        """Test initial state of login page"""
        login_page(self.mock_st)
        self.assertFalse(self.mock_st.session_state.get("logged_in", False))
        self.assertEqual(self.mock_st.session_state.get("page", "login"), "login")

    def test_login_with_valid_credentials(self):
        """Test login functionality with valid credentials"""
        # Mock successful authentication
        with patch("util.login_page.authenticate_user", return_value=True):
            login_page(self.mock_st)
            self.mock_st.session_state["email"] = "user@example.com"
            self.mock_st.session_state["password"] = "password123"
            self.assertTrue(self.mock_st.session_state.get("logged_in", False))

    def test_login_with_invalid_credentials(self):
        """Test login functionality with invalid credentials"""
        # Mock failed authentication
        with patch("util.login_page.authenticate_user", return_value=False):
            login_page(self.mock_st)
            self.mock_st.session_state["email"] = "wrong@example.com"
            self.mock_st.session_state["password"] = "wrongpass"
            self.assertFalse(self.mock_st.session_state.get("logged_in", False))

    def test_redirect_to_signup(self):
        """Test redirection to signup page"""
        login_page(self.mock_st)
        self.mock_st.session_state["page"] = "signup"
        self.assertEqual(self.mock_st.session_state["page"], "signup")

    def test_empty_credentials(self):
        """Test login attempt with empty credentials"""
        login_page(self.mock_st)
        self.mock_st.session_state["email"] = ""
        self.mock_st.session_state["password"] = ""
        self.assertFalse(self.mock_st.session_state.get("logged_in", False))


if __name__ == "__main__":
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output="test-reports/xml"),
        failfast=False,
        buffer=False,
        catchbreak=False,
    )

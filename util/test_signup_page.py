import unittest
from unittest.mock import MagicMock, patch

import xmlrunner
from streamlit import session_state as st

from util.signup_page import signup_page


class TestSignupPage(unittest.TestCase):
    def setUp(self):
        """Setup test environment before each test"""
        st.clear()
        self.mock_st = MagicMock()
        self.mock_st.session_state = {}

    def test_signup_page_initial_state(self):
        """Test initial state of signup page"""
        signup_page(self.mock_st)
        self.assertFalse(self.mock_st.session_state.get("signed_up", False))
        self.assertEqual(self.mock_st.session_state.get("page", "signup"), "signup")

    def test_successful_signup(self):
        """Test successful signup process"""
        with patch("util.signup_page.create_user", return_value=True):
            signup_page(self.mock_st)
            self.mock_st.session_state["email"] = "newuser@example.com"
            self.mock_st.session_state["password"] = "newpassword123"
            self.mock_st.session_state["confirm_password"] = "newpassword123"
            self.assertTrue(self.mock_st.session_state.get("signed_up", False))

    def test_failed_signup(self):
        """Test failed signup process"""
        with patch("util.signup_page.create_user", return_value=False):
            signup_page(self.mock_st)
            self.mock_st.session_state["email"] = "existing@example.com"
            self.mock_st.session_state["password"] = "password123"
            self.mock_st.session_state["confirm_password"] = "password123"
            self.assertFalse(self.mock_st.session_state.get("signed_up", False))

    def test_password_mismatch(self):
        """Test signup with mismatched passwords"""
        signup_page(self.mock_st)
        self.mock_st.session_state["email"] = "user@example.com"
        self.mock_st.session_state["password"] = "password123"
        self.mock_st.session_state["confirm_password"] = "different123"
        self.assertFalse(self.mock_st.session_state.get("signed_up", False))

    def test_invalid_email(self):
        """Test signup with invalid email format"""
        signup_page(self.mock_st)
        self.mock_st.session_state["email"] = "invalid_email"
        self.mock_st.session_state["password"] = "password123"
        self.mock_st.session_state["confirm_password"] = "password123"
        self.assertFalse(self.mock_st.session_state.get("signed_up", False))


if __name__ == "__main__":
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output="test-reports/xml"),
        failfast=False,
        buffer=False,
        catchbreak=False,
    )

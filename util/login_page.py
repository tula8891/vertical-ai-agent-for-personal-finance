# Login page function with a single column layout
# Dummy credentials for login
DUMMY_EMAIL = "user@example.com"
DUMMY_PASSWORD = "password123"


def login_page(st):
    """
    Render the login page of the Streamlit application.

    This function displays a login form where users can input their email and password.
    It checks the input against dummy credentials and updates the session state upon
    successful login. If the login is successful, it redirects the user to the main page.
    Additionally, it provides an option for users to navigate to the signup page.

    Args:
        st: The Streamlit instance used to render the page elements.
    """
    st.title("Login")

    with st.container():
        with st.form(key="login_form"):
            st.subheader("Please log in to continue")

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submit_button = st.form_submit_button("Login")

            if submit_button:
                if email == DUMMY_EMAIL and password == DUMMY_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.page = "main"  # Redirect to the main page
                    st.success("Login successful!")
                else:
                    st.error("Invalid credentials. Please try again.")

        # Redirect to signup page if user doesn't have an account
        if st.button("Don't have an account? Sign Up"):
            st.session_state.page = "signup"

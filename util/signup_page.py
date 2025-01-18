# Signup page function
def signup_page(st):
    """
    Render the signup page of the Streamlit application.

    This function creates a user-friendly signup form with email validation,
    password confirmation, and intuitive error messaging. It stores user
    information in the session state upon successful signup.

    Args:
        st: Streamlit instance for rendering UI components

    Features:
        - Email validation (requires '@' symbol)
        - Password confirmation check
        - Empty field validation
        - Intuitive error messages
        - Session state management
    """

    # Center-aligned container
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Sign Up")
        st.write("Create your account to get started.")

        # Signup form
        with st.form("signup_form", clear_on_submit=True):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input(
                "Password", type="password", placeholder="Create a password"
            )
            confirm_password = st.text_input(
                "Confirm Password", type="password", placeholder="Confirm your password"
            )

            # Full-width signup button
            if st.form_submit_button("Sign Up", use_container_width=True):
                if not email or "@" not in email:
                    st.error("Please enter a valid email address.")
                elif not password:
                    st.error("Please enter a password.")
                elif password != confirm_password:
                    st.error("Passwords do not match. Please try again.")
                else:
                    # Store user details in session state for demo purposes
                    st.session_state.user_email = email
                    st.session_state.page = "login"
                    st.success("Signup successful! Please log in.")

        # Login link
        st.write("Already have an account?")
        if st.button("Login", use_container_width=True):
            st.session_state.page = "login"

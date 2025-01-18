# Login page function with a single column layout
# Dummy credentials for login
DUMMY_EMAIL = "user@example.com"
DUMMY_PASSWORD = "password123"


def login_page(st):
    """Render the login page of the Streamlit application."""

    # Center-aligned container
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Login")
        st.write("Welcome back! Please log in to continue.")

        # Login form
        with st.form("login_form", clear_on_submit=True):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input(
                "Password", type="password", placeholder="Enter your password"
            )

            # Full-width login button
            if st.form_submit_button("Login", use_container_width=True):
                if email == DUMMY_EMAIL and password == DUMMY_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.username = "Demo User"
                    st.session_state.email = email
                    st.session_state.page = "main"
                    st.success("Login successful!")
                else:
                    st.error("Invalid credentials. Please try again.")

        # Sign up link
        st.write("Don't have an account?")
        if st.button("Sign Up", use_container_width=True):
            st.session_state.page = "signup"

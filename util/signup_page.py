
# Signup page function
def signup_page(st):
    st.title("Sign Up")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    submit_button = st.button("Sign Up")

    if submit_button:
        if password == confirm_password:
            st.session_state.page = "login"  # Redirect to login page after signup
            st.success("Signup successful! Please log in.")
        else:
            st.error("Passwords do not match. Please try again.")

    # Redirect to login page if user already has an account
    if st.button("Already have an account? Login"):
        st.session_state.page = "login"
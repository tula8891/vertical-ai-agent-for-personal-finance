# Import necessary libraries for the application
import streamlit as st
from snowflake.core import Root
from snowflake.cortex import Complete
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

from util.login_page import login_page
from util.signup_page import signup_page

# List of available models
MODELS = [
    "mistral-large2",
    "llama3.1-70b",
    "llama3.1-8b",
]

# Configure Streamlit page settings
st.set_page_config(
    page_title="Finance App",
    page_icon="💰",
    layout="centered",  # Using centered layout for better form display
    initial_sidebar_state="expanded",
)

# Use Streamlit's built-in theme configuration
st.markdown(
    """
    <style>
        /* Minimal custom styling */
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
        }
        .stForm {
            padding: 1rem;
            border-radius: 0.5rem;
        }
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)


# Helper function to initialize the Snowflake session once
def initialize_session():
    """
    Initialize a Snowflake session for the Streamlit application.

    This function checks if a Snowflake session is already initialized in the session state.
    If not, it creates a new session using the connection parameters from Streamlit secrets
    and stores it in the session state.

    Returns:
        The initialized Snowflake session stored in the session state.
    """
    if "session" not in st.session_state:
        connection_params = {
            "account": st.secrets["myconnection"]["account"],
            "user": st.secrets["myconnection"]["user"],
            "password": st.secrets["myconnection"]["password"],
            "warehouse": st.secrets["myconnection"]["warehouse"],
            "database": st.secrets["myconnection"]["database"],
            "schema": st.secrets["myconnection"]["schema"],
        }
        st.session_state.session = Session.builder.configs(connection_params).create()
    return st.session_state.session


# Main page function
def main_page():
    """
    Main page of the Streamlit application that displays the chat interface,
    manages user login/logout, and handles chat interactions with the Snowflake Cortex.
    It also initializes session state variables and displays chat messages from history.
    """
    # Custom CSS for sidebar
    st.markdown(
        """
        <style>
        .sidebar-button {
            background-color: #4B8BBE;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            margin: 0.5rem 0;
            width: 100%;
            text-align: left;
        }
        .sidebar .stButton>button {
            background-color: #4B8BBE;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            width: 100%;
            margin: 4px 0;
            text-align: left;
            font-size: 16px;
        }
        .sidebar .stButton>button:hover {
            background-color: #3D7BA8;
            border: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Add navigation bar with improved spacing
    nav_col1, nav_col2, nav_col3 = st.columns([6, 2, 2])
    with nav_col1:
        st.title("Econo Genie")
        st.caption("Personal Finance BRO")
    with nav_col3:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

    st.markdown("---")

    # Add profile section with improved spacing
    with st.expander("Your Investment Profile", expanded=True):
        st.markdown(
            """
            <style>
                div[data-testid="stExpander"] div[role="button"] p {
                    font-size: 1.1rem;
                    margin-bottom: 0.5rem;
                }
                div.row-widget.stRadio > div {
                    flex-direction: column;
                    gap: 0.5rem;
                }
                div.row-widget.stMultiSelect > div {
                    margin-top: 0.5rem;
                }
            </style>
        """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("##### Risk Profile")
            st.write("")  # Add spacing
            risk_profile = st.radio(
                "Select your risk tolerance",
                ["Conservative", "Moderate", "Moderately Aggressive"],
                label_visibility="collapsed",
            )

        with col2:
            st.markdown("##### Financial Goals")
            st.write("")  # Add spacing
            goals = st.multiselect(
                "Choose your financial goals",
                [
                    "House Down Payment",
                    "Retirement",
                    "Education",
                    "Emergency Fund",
                    "Wealth Building",
                ],
                default=["Retirement"],
                label_visibility="collapsed",
            )

        with col3:
            st.markdown("##### Investment Horizon")
            st.write("")  # Add spacing
            horizon = st.radio(
                "Select your investment timeline",
                [
                    "Short-term (1-3 years)",
                    "Medium-term (3-7 years)",
                    "Long-term (7+ years)",
                ],
                label_visibility="collapsed",
            )

        # Save preferences to session state
        if "risk_profile" not in st.session_state:
            st.session_state.risk_profile = risk_profile
        if "financial_goals" not in st.session_state:
            st.session_state.financial_goals = goals
        if "investment_horizon" not in st.session_state:
            st.session_state.investment_horizon = horizon

    st.markdown("---")

    # Add sidebar
    with st.sidebar:
        st.title("EconoGenie")
        st.markdown("### Personal Finance App")

        st.markdown("---")

        if st.button(
            "📚 Financial Literacy", use_container_width=True, key="sidebar_fin_lit"
        ):
            st.session_state.current_section = "financial_literacy"
            st.rerun()

        if st.button(
            "💰 Personalized Investment", use_container_width=True, key="sidebar_invest"
        ):
            st.session_state.current_section = "investment"
            st.rerun()

        if st.button("🤖 AI Agents [Beta]", use_container_width=True, key="sidebar_ai"):
            st.session_state.current_section = "ai_agents"
            st.rerun()

        st.markdown("---")

        # Add logout button at the bottom of sidebar
        st.markdown(
            """
            <style>
            [data-testid="stSidebarNav"] {
                background-image: linear-gradient(#4B8BBE, #3D7BA8);
                color: white;
                padding: 1rem;
                margin-top: auto;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🚪 Logout", key="sidebar_logout"):
            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()

    # Initialize session state for current section if not exists
    if "current_section" not in st.session_state:
        st.session_state.current_section = "financial_literacy"

    # Main content area
    if st.session_state.current_section == "financial_literacy":
        st.header("📚 Financial Literacy")
        st.markdown(
            """
        Welcome to your financial education hub! Here you can:
        - Take financial literacy assessments
        - Track your learning progress
        - Get personalized learning recommendations
        - Access educational resources
        """
        )

    elif st.session_state.current_section == "investment":
        st.header("💰 Personalized Investment Recommendations")
        st.markdown(
            """
        Get tailored investment advice based on your profile:
        - Risk assessment
        - Portfolio analysis
        - Investment suggestions
        - Market insights
        """
        )

    elif st.session_state.current_section == "ai_agents":
        st.header("🤖 AI Agents [Beta]")
        st.markdown(
            """
        Your AI-powered financial assistant:
        - Smart financial planning
        - Automated insights
        - Personalized recommendations
        - Real-time assistance
        """
        )

    # Ensure the Snowflake session is initialized
    initialize_session()

    # Display a welcome message
    st.write("Welcome to the main page!")

    # Initialize session state variables if not set
    init_service_metadata()
    init_config_options()
    init_messages()

    # Define icons for the chat messages
    icons = {"assistant": "❄️", "user": "👤"}

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.markdown(message["content"])

    # Check if the chat is disabled
    disable_chat = (
        "service_metadata" not in st.session_state
        or len(st.session_state.service_metadata) == 0
    )
    if question := st.chat_input("Ask a question...", disabled=disable_chat):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        # Display user message in chat message container
        with st.chat_message("user", avatar=icons["user"]):
            st.markdown(question.replace("$", "\$"))

        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar=icons["assistant"]):
            message_placeholder = st.empty()
            question = question.replace("'", "")
            prompt, results = create_prompt(question)
            with st.spinner("Thinking..."):
                generated_response = complete(st.session_state.model_name, prompt)
                # build references table for citation
                markdown_table = (
                    "###### References \n\n| PDF Title | URL |\n|-------|-----|\n"
                )
                for ref in results:
                    markdown_table += f"| {ref['chunk']}  |\n"
                message_placeholder.markdown(
                    generated_response + "\n\n" + markdown_table
                )

        st.session_state.messages.append(
            {"role": "assistant", "content": generated_response}
        )


# Your original helper functions
def init_messages():
    """
    Initialize the chat messages in the session state.

    This function checks if the 'clear_conversation' flag is set or if 'messages'
    is not present in the session state. If either condition is true, it initializes
    the 'messages' list in the session state.
    """
    if st.session_state.clear_conversation or "messages" not in st.session_state:
        st.session_state.messages = []


def init_service_metadata():
    """
    Initialize service metadata for the Snowflake Cortex search services.

    This function ensures that a Snowflake session is initialized and retrieves service
    metadata from the Snowflake session. It populates the session state with the metadata
    of available Cortex search services.
    """
    session = initialize_session()
    if "service_metadata" not in st.session_state:
        services = session.sql("SHOW CORTEX SEARCH SERVICES;").collect()
        service_metadata = []
        if services:
            for s in services:
                svc_name = s["name"]
                svc_search_col = session.sql(
                    f"DESC CORTEX SEARCH SERVICE {svc_name};"
                ).collect()[0]["search_column"]
                service_metadata.append(
                    {"name": svc_name, "search_column": svc_search_col}
                )
        st.session_state.service_metadata = service_metadata


def init_config_options():
    """
    Initialize the configuration options for the Streamlit application.

    This function sets up the sidebar configuration options, including the selection
    of Cortex search services, model selection, and advanced options for chat history
    and context chunk settings.
    """
    st.sidebar.selectbox(
        "Select cortex search service:",
        [s["name"] for s in st.session_state.service_metadata],
        key="selected_cortex_search_service",
    )
    st.sidebar.button("Clear conversation", key="clear_conversation")
    st.sidebar.toggle("Debug", key="debug", value=False)
    st.sidebar.toggle("Use chat history", key="use_chat_history", value=True)

    with st.sidebar.expander("Advanced options"):
        st.selectbox("Select model:", MODELS, key="model_name")
        st.number_input(
            "Select number of context chunks",
            value=5,
            key="num_retrieved_chunks",
            min_value=1,
            max_value=10,
        )
        st.number_input(
            "Select number of messages to use in chat history",
            value=5,
            key="num_chat_messages",
            min_value=1,
            max_value=10,
        )


# Corrected query_cortex_search_service function
def query_cortex_search_service(query, columns=[], filter={}):
    """
    Perform a search query on the selected Cortex search service.

    This function initializes a Snowflake session and accesses the selected Cortex
    search service. It performs a search using the provided query and columns, and
    constructs a context string from the search results.

    Args:
        query (str): The search query string.
        columns (list): The list of columns to include in the search.
        filter (dict): Optional filters for the search query.

    Returns:
        tuple: A tuple containing the context string and the search results.
    """
    session = initialize_session()
    db, schema = session.get_current_database(), session.get_current_schema()

    root = Root(session)

    cortex_search_service = (
        root.databases[db]
        .schemas[schema]
        .cortex_search_services[st.session_state.selected_cortex_search_service]
    )
    context_documents = cortex_search_service.search(
        query,
        columns=["chunk", "company_name"],
        limit=st.session_state.num_retrieved_chunks,
    )

    results = context_documents.results
    service_metadata = st.session_state.service_metadata
    search_col = [
        s["search_column"]
        for s in service_metadata
        if s["name"] == st.session_state.selected_cortex_search_service
    ][0].lower()

    context_str = ""
    for i, r in enumerate(results):
        context_str += f"Context document {i + 1}: {r[search_col]} \n" + "\n"

    if st.session_state.debug:
        st.sidebar.text_area("Context documents", context_str, height=500)

    return context_str, results


def get_chat_history():
    """
    Retrieve the chat history from the session state.

    This function fetches the last few chat messages based on the configured number
    of messages to use in the chat history.

    Returns:
        list: A list of chat messages from the session state.
    """
    start_index = max(
        0, len(st.session_state.messages) - st.session_state.num_chat_messages
    )
    return st.session_state.messages[start_index : len(st.session_state.messages) - 1]


def complete(model, prompt):
    """
    Generate a completion response using the specified model and prompt.

    This function uses the Snowflake Cortex Complete function to generate a response
    based on the provided model and prompt.

    Args:
        model (str): The name of the model to use for completion.
        prompt (str): The prompt string to generate a response for.

    Returns:
        str: The generated completion response.
    """
    return Complete(model, prompt).replace("$", "\$")


def make_chat_history_summary(chat_history, question):
    """
    Create a prompt to generate a query based on chat history and the current question.

    This function constructs a prompt that extends the user's question with the provided
    chat history, aiming to generate a natural language query.

    Args:
        chat_history (str): The chat history to include in the prompt.
        question (str): The current question from the user.

    Returns:
        str: The constructed prompt for generating a query.
    """
    prompt = f"""
        [INST]
        Based on the chat history below and the question, generate a query that extend the question
        with the chat history provided. The query should be in natural language.
        Answer with only the query. Do not add any explanation.

        <chat_history>
        {chat_history}
        </chat_history>
        <question>
        {question}
        </question>
        [/INST]
    """

    return complete(st.session_state.model_name, prompt)


def create_prompt(user_question):
    """
    Create a prompt for the chatbot based on the user's question and chat history.

    This function checks if chat history should be used and constructs a prompt
    accordingly. It performs a search query using the generated prompt and returns
    the prompt context and search results.

    Args:
        user_question (str): The question from the user to create a prompt for.

    Returns:
        tuple: A tuple containing the prompt context and search results.
    """
    if st.session_state.use_chat_history:
        chat_history = get_chat_history()
        if chat_history != []:
            question_summary = make_chat_history_summary(chat_history, user_question)
            prompt_context, results = query_cortex_search_service(
                question_summary,
                columns=["chunk"],
                filter={},
            )
        else:
            prompt_context, results = query_cortex_search_service(
                user_question,
                columns=["chunk"],
                filter={},
            )
            chat_history = ""
    else:
        prompt_context, results = query_cortex_search_service(
            user_question,
            columns=["chunk"],
            filter={},
        )
        chat_history = ""

    return prompt_context, results


def landing_page():
    """
    Landing page of the Streamlit application that introduces the app and its features.
    """
    # Set up the page layout

    # Custom CSS for styling (without hardcoding colors)
    st.markdown(
        """
        <style>
            /* Center align text and buttons */
            .stButton>button {
                width: 100%;
                margin-top: 1rem;
                font-weight: bold;
                border-radius: 0.5rem;
                padding: 0.5rem 1rem;
            }
            /* Hide Streamlit branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Add spacing between sections */
            .section {
                margin-bottom: 2rem;
            }
            /* Custom font size for headers */
            h1 {
                font-size: 2.5rem;
                text-align: center;
            }
            h2 {
                font-size: 1.8rem;
                margin-bottom: 1rem;
            }
            h3 {
                font-size: 1.5rem;
                margin-bottom: 0.5rem;
            }
            p {
                font-size: 1.1rem;
                line-height: 1.6;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Navigation Bar
    col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 2])
    with col1:
        st.markdown("### Econo Genie")
    with col3:
        if st.button("Home", key="nav_home_btn", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
    with col4:
        if st.button("Login", key="nav_login_btn", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    with col5:
        if st.button("Sign Up", key="nav_signup_btn", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()

    st.markdown("---")

    # Custom CSS for landing page buttons
    st.markdown(
        """
        <style>
            .stButton>button {
                font-size: 16px;
                padding: 2px 10px;
                border-radius: 4px;
                height: 35px;
                width: 100%;
                margin: 0;
            }
            .button-col {
                display: flex;
                justify-content: center;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Personalized Investment Recommendations Section
    st.markdown("## Personalized Investment Recommendations")
    st.markdown(
        """
        **Tailored advice based on your financial profile.**

        We offer a wide range of investments, including stocks, bonds, mutual funds, and more.
        """
    )
    col1, col2, col3 = st.columns([12, 5, 4])
    with col2:
        if st.button("Start now", key="start_investment", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()

    st.markdown("---")

    # Financial Literacy Section
    st.markdown("## Financial Literacy")
    st.markdown(
        """
        **Assessment, progress tracking, and suggestions on what to learn next.**

        We offer a wide range of resources, including articles, videos, and quizzes.
        """
    )
    col1, col2, col3 = st.columns([12, 5, 4])
    with col2:
        if st.button(
            "Explore now", key="explore_financial_literacy", use_container_width=True
        ):
            st.session_state.page = "signup"
            st.rerun()

    st.markdown("---")

    # AI Agents Section
    st.markdown("## AI Agents [Work in Progress]")
    st.markdown(
        """
        **The AI Financial Assistant is like having a smart, friendly money coach in your pocket.**

        It's designed to make managing your day-to-day finances simple, stress-free, and even fun.
        """
    )
    col1, col2, col3 = st.columns([12, 5, 4])
    with col2:
        if st.button("Explore now", key="explore_ai_agents", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()

    st.markdown("---")
    # Custom CSS for styling
    st.markdown(
        """
        <style>
            /* Center align text and buttons */
            .stButton>button {
                width: 100%;
                margin-top: 1rem;
                background-color: #4B8BBE;
                color: white;
                font-weight: bold;
                border-radius: 0.5rem;
                padding: 0.5rem 1rem;
            }
            .stButton>button:hover {
                background-color: #306998;
            }
            /* Hide Streamlit branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Add spacing between sections */
            .section {
                margin-bottom: 2rem;
            }
            /* Custom font size for headers */
            h1 {
                font-size: 2.5rem;
                text-align: center;
            }
            h2 {
                font-size: 1.8rem;
                margin-bottom: 1rem;
            }
            h3 {
                font-size: 1.5rem;
                margin-bottom: 0.5rem;
            }
            p {
                font-size: 1.1rem;
                line-height: 1.6;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# Main function to handle page flow
def main():
    """
    Main function to handle the page flow of the Streamlit application.

    This function determines the current page in the session state and displays
    the appropriate page (landing, login, signup, or main page) based on the user's state.
    """
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "login":
        login_page(st)
    elif st.session_state.page == "signup":
        signup_page(st)
    else:
        main_page()


if __name__ == "__main__":
    main()

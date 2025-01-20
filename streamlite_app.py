import logging

import streamlit as st
from snowflake.core import Root
from snowflake.cortex import Complete
from snowflake.snowpark import Session

# Import utility functions
from util.login_page import login_page
from util.signup_page import signup_page

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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
    layout="centered",
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
    """
    logging.info("Initializing Snowflake session.")
    if "session" not in st.session_state:
        logging.info(
            "Snowflake session not found in session state, creating a new one."
        )
        connection_params = {
            "account": st.secrets["myconnection"]["account"],
            "user": st.secrets["myconnection"]["user"],
            "password": st.secrets["myconnection"]["password"],
            "warehouse": st.secrets["myconnection"]["warehouse"],
            "database": st.secrets["myconnection"]["database"],
            "schema": st.secrets["myconnection"]["schema"],
        }
        try:
            st.session_state.session = Session.builder.configs(
                connection_params
            ).create()
            logging.info("Snowflake session created successfully.")
        except Exception as e:
            logging.error(f"Error creating Snowflake session: {e}")
            st.error("Failed to connect to Snowflake. Please check your credentials.")
            return None
    else:
        logging.info("Snowflake session found in session state.")
    return st.session_state.session


# Main page function
def main_page():
    """
    Main page of the Streamlit application that displays the chat interface,
    manages user login/logout, and handles chat interactions with the Snowflake Cortex.
    It also initializes session state variables and displays chat messages from history.
    """
    logging.info("Displaying main page.")

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
            logging.info(
                "Logout button clicked. Clearing session state and redirecting to login page."
            )
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
        logging.info(
            f"User profile - Risk: {risk_profile}, Goals: {goals}, Horizon: {horizon}"
        )

    st.markdown("---")

    # Add sidebar
    with st.sidebar:
        st.title("EconoGenie")
        st.markdown("### Personal Finance App")

        st.markdown("---")

        if st.button(
            "📚 Financial Literacy", use_container_width=True, key="sidebar_fin_lit"
        ):
            logging.info("Sidebar button 'Financial Literacy' clicked.")
            st.session_state.current_section = "financial_literacy"
            st.rerun()

        if st.button(
            "💰 Personalized Investment", use_container_width=True, key="sidebar_invest"
        ):
            logging.info("Sidebar button 'Personalized Investment' clicked.")
            st.session_state.current_section = "investment"
            st.rerun()

        if st.button("🤖 AI Agents [Beta]", use_container_width=True, key="sidebar_ai"):
            logging.info("Sidebar button 'AI Agents' clicked.")
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
            logging.info(
                "Sidebar logout button clicked, logging out user and navigating to landing page"
            )
            st.session_state.clear()
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
    logging.info(f"Current section displayed: {st.session_state.current_section}")

    # Display a welcome message
    st.write("Welcome to the main page!")

    # Initialize session state variables if not set
    init_service_metadata()
    init_config_options()
    init_messages()

    # Define icons for the chat messages
    icons = {"assistant": "❄️", "user": "👤"}

    # Display chat messages from history on app rerun
    if "messages" in st.session_state and st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=icons[message["role"]]):
                st.markdown(message["content"])

    # Check if the chat is disabled
    disable_chat = (
        "service_metadata" not in st.session_state
        or len(st.session_state.service_metadata) == 0
    )
    if question := st.chat_input("Ask a question...", disabled=disable_chat):
        logging.info(f"User input received: {question}")
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        # Display user message in chat message container
        with st.chat_message("user", avatar=icons["user"]):
            st.markdown(question.replace("$", "\$"))

        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar=icons["assistant"]):
            message_placeholder = st.empty()
            question = question.replace("'", "")
            try:
                prompt, results = create_prompt(question)
                with st.spinner("Thinking..."):
                    generated_response = complete(
                        st.session_state.model_name,
                        prompt,
                        session=st.session_state.session,
                    )
                    # build references table for citation
                    markdown_table = (
                        "###### References \n\n| PDF Title | URL |\n|-------|-----|\n"
                    )
                    for ref in results:
                        markdown_table += f"| {ref['chunk']} | {ref.get('company_name', 'N/A')} |\n"  # added the company name
                    message_placeholder.markdown(
                        generated_response + "\n\n" + markdown_table
                    )
                logging.info(f"Assistant generated response: {generated_response}")
            except Exception as e:
                logging.error(f"Error during chat completion: {e}")
                message_placeholder.markdown(
                    "An error occurred while processing your request."
                )
                generated_response = "An error occurred."

        st.session_state.messages.append(
            {"role": "assistant", "content": generated_response}
        )


# Your original helper functions
def init_messages():
    """
    Initialize the chat messages in the session state.
    """
    logging.info("Initializing chat messages.")
    if (
        st.session_state.get("clear_conversation", False)
        or "messages" not in st.session_state
    ):
        st.session_state.messages = []
        logging.info("Chat messages initialized or cleared.")


def init_service_metadata():
    """
    Initialize service metadata for the Snowflake Cortex search services.
    """
    logging.info("Initializing service metadata.")
    if "service_metadata" not in st.session_state:
        try:
            session = st.session_state.session
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
            logging.info(
                f"Service metadata initialized: {st.session_state.service_metadata}"
            )
        except Exception as e:
            logging.error(f"Error fetching service metadata: {e}")
            st.error("An error occurred while fetching service metadata. Check logs.")
            st.session_state.service_metadata = []
    else:
        logging.info("Service metadata already present in session state.")


def init_config_options():
    """
    Initialize the configuration options for the Streamlit application.
    """
    logging.info("Initializing config options.")

    # Set the model name based on current section
    if "current_section" in st.session_state:
        if st.session_state.current_section == "financial_literacy":
            st.session_state.model_name = "mistral-large2"
            st.session_state.selected_cortex_search_service = "EDU_SERVICE"
        else:  # investment or ai_agents
            st.session_state.model_name = "mistral-large2"
            st.session_state.selected_cortex_search_service = "FIN_SERVICE"
    else:
        st.session_state.model_name = "mistral-large2"
        st.session_state.selected_cortex_search_service = "EDU_SERVICE"

    # Initialize other config options if not already set
    if "use_chat_history" not in st.session_state:
        st.session_state.use_chat_history = True
    if "num_retrieved_chunks" not in st.session_state:
        st.session_state.num_retrieved_chunks = 5


def query_cortex_search_service(query, columns=[], filter={}):
    """
    Perform a search query on the selected Cortex search service, including 'company_name' and 'chunk'.
    """
    logging.info(
        f"Querying cortex search service with query: {query}, columns: {columns}, filter: {filter}"
    )
    session = st.session_state.session
    if not session:
        return "", []
    db, schema = session.get_current_database(), session.get_current_schema()

    root = Root(session)

    try:
        cortex_search_service = (
            root.databases[db]
            .schemas[schema]
            .cortex_search_services[st.session_state.selected_cortex_search_service]
        )
        logging.info(f"Selected cortex search service: {cortex_search_service}")
        # Changed to include all columns
        context_documents = cortex_search_service.search(
            query,
            columns=["chunk"],  # Include both chunk and company_name
            limit=st.session_state.num_retrieved_chunks,
        )

        results = context_documents.results

        context_str = ""
        for i, r in enumerate(results):
            context_str += (
                f"Context document {i + 1}: {r['chunk']} (Company: {r.get('company_name', 'N/A')}) \n"
                + "\n"
            )

        if st.session_state.debug:
            st.sidebar.text_area("Context documents", context_str, height=500)
        logging.info(
            f"Cortex search service query successful, found {len(results)} documents"
        )

        return context_str, results
    except Exception as e:
        logging.error(f"Error querying cortex search service: {e}")
        st.error("An error occured while fetching the data, please check logs")
        return "", []


def get_chat_history():
    """
    Retrieve the chat history from the session state.
    """
    logging.info("Retrieving chat history.")
    if "messages" not in st.session_state:
        logging.warning("No chat messages found in session state")
        return []
    start_index = max(
        0, len(st.session_state.messages) - st.session_state.num_chat_messages
    )
    history = st.session_state.messages[
        start_index : len(st.session_state.messages) - 1
    ]
    logging.info(f"Retrieved {len(history)} chat messages.")
    return history


def complete(model, prompt, session=None):
    """
    Generate a completion response using the specified model and prompt.
    """
    logging.info(f"Generating completion with model: {model}, prompt: {prompt}")
    try:
        response = Complete(model, prompt, session=session).replace("$", "\$")
        logging.info("Completion generated successfully.")
        return response
    except Exception as e:
        logging.error(f"Error during completion: {e}")
        st.error("An error occurred during completion. Check logs.")
        return "An error occurred."


def make_chat_history_summary(chat_history, question):
    """
    Create a prompt to generate a query based on chat history and the current question.
    """
    logging.info("Creating chat history summary prompt.")
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
    logging.info("Chat history summary prompt created, using LLM to process")
    return complete(
        st.session_state.model_name, prompt, session=st.session_state.session
    )


def create_prompt(user_question):
    """
    Create a prompt for the chatbot based on the user's question and chat history.
    """
    logging.info(f"Creating prompt with user question: {user_question}")
    if st.session_state.use_chat_history:
        logging.info("Using chat history.")
        chat_history = get_chat_history()
        if chat_history:
            question_summary = make_chat_history_summary(chat_history, user_question)
            logging.info(
                f"Summary of the question: {question_summary}"
            )  # Add log for summary
            prompt_context, results = query_cortex_search_service(
                question_summary,
                columns=["chunk", "company_name"],  # ADD COMPANY NAME
                filter={},
            )
            logging.info("Chat history used and query processed.")
        else:
            prompt_context, results = query_cortex_search_service(
                user_question,
                columns=["chunk", "company_name"],  # ADD COMPANY NAME
                filter={},
            )
            logging.info(
                "No chat history found, using the current user question for query"
            )
            chat_history = ""
    else:
        logging.info("Not using chat history.")
        prompt_context, results = query_cortex_search_service(
            user_question,
            columns=["chunk", "company_name"],  # ADD COMPANY NAME
            filter={},
        )
        chat_history = ""
        logging.info("Query processed without chat history.")

    logging.info(f"Prompt context: {prompt_context}")
    logging.info(f"Results: {results}")
    prompt = f"""
        [INST]

        You are an expert educator with years of experience in teaching and providing constructive feedback. Below, I will provide a set of quiz questions along with the correct answers and a student's responses. Your task is to:
        Evaluate the student's answers: Compare the student's responses to the correct answers and determine if they are correct, partially correct, or incorrect.
        Provide detailed feedback: For each question, explain why the student's answer is correct or incorrect. If the answer is partially correct, highlight what was right and what was missing. If the answer is incorrect, provide a clear explanation of the correct concept.
        Suggest further reading: For questions the student answered incorrectly or partially correctly, recommend specific topics, concepts, or resources (e.g., chapters, articles, videos) the student should review to improve their understanding.
        Here is the quiz content, correct answers, and the student's responses

        <chat_history>
        {chat_history}
        </chat_history>
        <context>
        {prompt_context}
        </context>
        <question>
        {user_question}
        </question>
        [/INST]
        Answer:
        """

    return prompt, results


def landing_page():
    """
    Landing page of the Streamlit application that introduces the app and its features.
    """
    logging.info("Displaying landing page.")
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
            logging.info("Landing page button 'Home' clicked.")
            st.session_state.page = "landing"
            st.rerun()
    with col4:
        if st.button("Login", key="nav_login_btn", use_container_width=True):
            logging.info("Landing page button 'Login' clicked.")
            st.session_state.page = "login"
            st.rerun()
    with col5:
        if st.button("Sign Up", key="nav_signup_btn", use_container_width=True):
            logging.info("Landing page button 'Sign Up' clicked.")
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
            logging.info("Landing page button 'Start now' (invest) clicked.")
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
            logging.info("Landing page button 'Explore now' (fin lit) clicked.")
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
            logging.info("Landing page button 'Explore now' (AI) clicked.")
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
    """
    logging.info("Starting the application.")
    if "page" not in st.session_state:
        st.session_state.page = "landing"
        logging.info("No page found in session state, defaulting to landing page.")

    # Initialize session here
    if "session" not in st.session_state:
        session = initialize_session()
        if not session:
            return  # Stop if session cannot be initialized

    if st.session_state.page == "landing":
        logging.info("Displaying landing page.")
        landing_page()
    elif st.session_state.page == "login":
        logging.info("Displaying login page.")
        login_page(st)
    elif st.session_state.page == "signup":
        logging.info("Displaying signup page.")
        signup_page(st)
    else:
        # Corrected the multiple logging of the main page by checking if the page has changed in session.
        if (
            "previous_page" not in st.session_state
            or st.session_state.previous_page != "main"
        ):
            logging.info("Displaying main page.")
            st.session_state.previous_page = (
                "main"  # Setting the previous page to main to avoid multiple logging.
            )
        main_page()


if __name__ == "__main__":
    main()

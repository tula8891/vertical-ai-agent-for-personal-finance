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

# Custom CSS for minimalist, professional look
st.markdown(
    """
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f7f7f7;
            margin: 0;
            padding: 0;
        }
        .login-container {
            background: white;
            padding: 30px 40px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            margin: 0 auto;
            text-align: center;
        }
        .login-container h2 {
            margin-bottom: 20px;
            font-size: 22px;
            color: #333;
        }
        .login-container input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
        }
        .login-container button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        .login-container button:hover {
            background-color: #45a049;
        }
        .signup-link {
            color: #007bff;
            font-size: 14px;
            text-decoration: none;
        }
        .signup-link:hover {
            text-decoration: underline;
        }
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
    Render the main page of the Streamlit application.

    This function sets up the main page interface, initializes the Snowflake session,
    manages user login/logout, and handles chat interactions with the Snowflake Cortex.
    It also initializes session state variables and displays chat messages from history.
    """
    st.title(f":speech_balloon: Welcome to EconoGenie: Your Personal Finance Bro")

    # Ensure the Snowflake session is initialized
    session = initialize_session()

    # Display a welcome message
    st.write("Welcome to the main page!")

    # Logout button
    if st.button("Logout"):
        # Set the logged_in state to False and redirect to the login page
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.success("Logged out successfully!")

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


def main():
    """
    Main function to handle the page flow of the Streamlit application.

    This function determines the current page in the session state and displays
    the appropriate page (login, signup, or main page) based on the user's state.
    """
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "login":
        login_page(st)
    elif st.session_state.page == "signup":
        signup_page(st)
    else:
        main_page()


if __name__ == "__main__":
    main()

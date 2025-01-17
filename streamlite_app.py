import streamlit as st
from snowflake.core import Root
from snowflake.cortex import Complete
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
from util.login_page import login_page
from util.signup_page import signup_page
import toml

# Load the TOML configuration file
#config = toml.load('config.toml')

# List of available models
MODELS = [
    "mistral-large2",
    "llama3.1-70b",
    "llama3.1-8b",
]

# Custom CSS for minimalist, professional look
st.markdown("""
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
""", unsafe_allow_html=True)


# Helper function to initialize the Snowflake session once
def initialize_session():
    # Check if the session is already initialized in the session state
    if 'session' not in st.session_state:
        # Create and store the session in session_state
        # st.session_state.session = Session.builder.config("connection_name", "myconnection").create()
        # Ensure you pass the whole configuration dictionary to the builder
        # connection_params = config['myconnection']  # Get the configuration dictionary for the connection
        connection_params = {
    'account': st.secrets["myconnection"]["account"],
    'user': st.secrets["myconnection"]["user"],
    'password': st.secrets["myconnection"]["password"],
    'warehouse': st.secrets["myconnection"]["warehouse"],
    'database': st.secrets["myconnection"]["database"],
    'schema': st.secrets["myconnection"]["schema"],
}
        # Initialize the session with the configuration dictionary
        st.session_state.session = Session.builder.configs(connection_params).create()
    return st.session_state.session


# Main page function
def main_page():
    st.title(f":speech_balloon: Chatbot with Snowflake Cortex")

    session = initialize_session()  # Ensure session is initialized

    st.write("Welcome to the main page!")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"  # Redirect to login page after logout
        st.success("Logged out successfully!")

    # Initialize session state variables if not set
    init_service_metadata()
    init_config_options()
    init_messages()

    icons = {"assistant": "❄️", "user": "👤"}

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.markdown(message["content"])

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
                generated_response = complete(
                    st.session_state.model_name, prompt
                )
                # build references table for citation
                markdown_table = "###### References \n\n| PDF Title | URL |\n|-------|-----|\n"
                for ref in results:
                    markdown_table += f"| {ref['chunk']}  |\n"
                message_placeholder.markdown(generated_response + "\n\n" + markdown_table)

        st.session_state.messages.append(
            {"role": "assistant", "content": generated_response}
        )


# Your original helper functions
def init_messages():
    if st.session_state.clear_conversation or "messages" not in st.session_state:
        st.session_state.messages = []


def init_service_metadata():
    session = initialize_session()  # Ensure session is initialized
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
    session = initialize_session()  # Ensure session is initialized
    db, schema = session.get_current_database(), session.get_current_schema()

    # Initialize 'root' using the active session
    root = Root(session)

    cortex_search_service = (
        root.databases[db]
            .schemas[schema]
            .cortex_search_services[st.session_state.selected_cortex_search_service]
    )
    context_documents = cortex_search_service.search(
        query, columns=["chunk", "company_name"], limit=st.session_state.num_retrieved_chunks
    )

    results = context_documents.results
    service_metadata = st.session_state.service_metadata
    search_col = [s["search_column"] for s in service_metadata
                  if s["name"] == st.session_state.selected_cortex_search_service][0].lower()

    context_str = ""
    for i, r in enumerate(results):
        context_str += f"Context document {i + 1}: {r[search_col]} \n" + "\n"

    if st.session_state.debug:
        st.sidebar.text_area("Context documents", context_str, height=500)

    return context_str, results


def get_chat_history():
    start_index = max(0, len(st.session_state.messages) - st.session_state.num_chat_messages)
    return st.session_state.messages[start_index : len(st.session_state.messages) - 1]


def complete(model, prompt):
    return Complete(model, prompt).replace("$", "\$")


def make_chat_history_summary(chat_history, question):
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

    summary = complete(st.session_state.model_name, prompt)

    if st.session_state.debug:
        st.sidebar.text_area(
            "Chat history summary", summary.replace("$", "\$"), height=150
        )

    return summary


def create_prompt(user_question):
    if st.session_state.use_chat_history:
        chat_history = get_chat_history()
        if chat_history != []:
            question_summary = make_chat_history_summary(chat_history, user_question)
            prompt_context, results = query_cortex_search_service(
                question_summary,
                columns=["chunk"],
                filter={"@and": [{"@eq": {"language": "English"}}]},
            )
        else:
            prompt_context, results = query_cortex_search_service(
                user_question,
                columns=["chunk"],
                filter={"@and": [{"@eq": {"language": "English"}}]},
            )
    else:
        prompt_context, results = query_cortex_search_service(
            user_question,
            columns=["chunk"],
            filter={"@and": [{"@eq": {"language": "English"}}]},
        )
        chat_history = ""

    prompt = f"""
            [INST]
            You are a helpful AI chat assistant with RAG capabilities. When a user asks you a question,
            you will also be given context provided between <context> and </context> tags. Use that context
            with the user's chat history provided in the between <chat_history> and </chat_history> tags
            to provide a summary that addresses the user's question. Ensure the answer is coherent, concise,
            and directly relevant to the user's question.

            If the user asks a generic question which cannot be answered with the given context or chat_history,
            just say "I don't know the answer to that question.

            Don't saying things like "according to the provided context".

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


# Main function to handle page flow
def main():
    # Set initial page if not set
    if "page" not in st.session_state:
        st.session_state.page = "login"  # Default to login page

    # Check if the user is logged in and display the corresponding page
    if st.session_state.page == "login":
        login_page(st)
    elif st.session_state.page == "signup":
        signup_page(st)
    elif st.session_state.page == "main":
        main_page()


if __name__ == "__main__":
    main()

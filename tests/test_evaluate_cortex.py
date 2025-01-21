"""
Test cases for Cortex Search Service evaluator.
"""
import os
from unittest.mock import MagicMock, Mock, patch

import pytest
from snowflake.core import Root
from snowflake.snowpark import Session
from trulens.connectors.snowflake import SnowflakeConnector
from trulens.core import TruSession

from evaluate_cortex import CortexSearchRetriever, RAG_from_scratch, connection_params


@pytest.fixture
def mock_snowpark_session():
    """Create a mock Snowpark session."""
    mock_session = Mock(spec=Session)
    return mock_session


@pytest.fixture
def mock_root():
    """Create a mock Root object with nested structure."""
    mock_root = Mock(spec=Root)

    # Mock the nested structure
    mock_db = Mock()
    mock_schema = Mock()
    mock_service = Mock()

    # Setup the chain
    mock_root.databases = {os.getenv("SNOWFLAKE_DATABASE"): mock_db}
    mock_db.schemas = {os.getenv("SNOWFLAKE_SCHEMA"): mock_schema}
    mock_schema.cortex_search_services = {os.getenv("SNOWFLAKE_CORTEX_SEARCH_SERVICE"): mock_service}

    return mock_root, mock_service


@pytest.fixture
def mock_tru_session():
    """Create a mock TruSession."""
    return Mock(spec=TruSession)


@pytest.fixture
def mock_snowflake_connector():
    """Create a mock SnowflakeConnector."""
    return Mock(spec=SnowflakeConnector)


def test_connection_params_structure():
    """Test that connection parameters have all required fields."""
    required_params = {
        "account",
        "user",
        "password",
        "role",
        "database",
        "schema",
        "warehouse",
    }
    assert set(connection_params.keys()) == required_params

    # Check that no values are None or empty
    for key, value in connection_params.items():
        assert value is not None, f"{key} should not be None"
        assert value != "", f"{key} should not be empty"


@pytest.mark.parametrize(
    "query,expected_results",
    [
        ("test query", ["result1", "result2"]),
        ("empty query", []),
    ],
)
def test_cortex_search_retriever_retrieve(mock_snowpark_session, mock_root, query, expected_results):
    """Test CortexSearchRetriever's retrieve method."""
    root_mock, service_mock = mock_root

    # Configure service mock
    if expected_results:
        service_mock.search.return_value = Mock(results=[{"CHUNK": result} for result in expected_results])
    else:
        service_mock.search.return_value = Mock(results=[])

    # Create retriever with mocked session
    retriever = CortexSearchRetriever(snowpark_session=mock_snowpark_session)

    # Patch Root creation to return our mock
    with patch("evaluate_cortex.Root", return_value=root_mock):
        results = retriever.retrieve(query)

    # Verify results
    assert results == expected_results

    # Verify search was called with correct parameters
    service_mock.search.assert_called_once_with(query=query, columns=["CHUNK"], limit=retriever._limit_to_retrieve)


def test_cortex_search_retriever_retrieve_error(mock_snowpark_session, mock_root):
    """Test error handling in retrieve method."""
    root_mock, service_mock = mock_root

    # Configure service mock to raise an exception
    service_mock.search.side_effect = Exception("Test error")

    # Create retriever with mocked session
    retriever = CortexSearchRetriever(snowpark_session=mock_snowpark_session)

    # Patch Root creation to return our mock
    with patch("evaluate_cortex.Root", return_value=root_mock):
        results = retriever.retrieve("test query")

    # Verify empty results on error
    assert results == []


def test_cortex_search_retriever_init():
    """Test CortexSearchRetriever initialization."""
    mock_session = Mock(spec=Session)
    limit = 5

    retriever = CortexSearchRetriever(snowpark_session=mock_session, limit_to_retrieve=limit)

    assert retriever._snowpark_session == mock_session
    assert retriever._limit_to_retrieve == limit


def test_cortex_search_retriever_invalid_response(mock_snowpark_session, mock_root):
    """Test handling of invalid response format."""
    root_mock, service_mock = mock_root

    # Configure service mock to return invalid response
    service_mock.search.return_value = None

    # Create retriever with mocked session
    retriever = CortexSearchRetriever(snowpark_session=mock_snowpark_session)

    # Patch Root creation to return our mock
    with patch("evaluate_cortex.Root", return_value=root_mock):
        results = retriever.retrieve("test query")

    # Verify empty results for invalid response
    assert results == []


def test_cortex_search_retriever_missing_results_attr(mock_snowpark_session, mock_root):
    """Test handling of response missing 'results' attribute."""
    root_mock, service_mock = mock_root

    # Configure service mock to return response without results
    service_mock.search.return_value = Mock(spec=[])

    # Create retriever with mocked session
    retriever = CortexSearchRetriever(snowpark_session=mock_snowpark_session)

    # Patch Root creation to return our mock
    with patch("evaluate_cortex.Root", return_value=root_mock):
        results = retriever.retrieve("test query")

    # Verify empty results when results attribute is missing
    assert results == []


@pytest.fixture
def mock_rag_dependencies(mock_snowpark_session, mock_snowflake_connector, mock_tru_session):
    """Create mock dependencies for RAG_from_scratch."""
    with patch("evaluate_cortex.SnowflakeConnector", return_value=mock_snowflake_connector), patch(
        "evaluate_cortex.TruSession", return_value=mock_tru_session
    ), patch("evaluate_cortex.create_snowpark_session", return_value=mock_snowpark_session):
        yield {
            "session": mock_snowpark_session,
            "connector": mock_snowflake_connector,
            "tru_session": mock_tru_session,
        }


def test_rag_from_scratch_init(mock_rag_dependencies):
    """Test RAG_from_scratch initialization."""
    rag = RAG_from_scratch()

    assert isinstance(rag.retriever, CortexSearchRetriever)
    assert rag.tru_snowflake_connector == mock_rag_dependencies["connector"]
    assert rag.tru_session == mock_rag_dependencies["tru_session"]


@pytest.mark.parametrize(
    "query,context,expected_completion",
    [
        ("test query", ["context1", "context2"], "test completion"),
        ("empty context", [], "No relevant information found"),
    ],
)
def test_rag_from_scratch_query(mock_rag_dependencies, query, context, expected_completion):
    """Test RAG_from_scratch query pipeline."""
    with patch("evaluate_cortex.Complete", return_value=expected_completion) as mock_complete:
        rag = RAG_from_scratch()

        # Mock retrieve_context
        with patch.object(rag, "retrieve_context", return_value=context):
            result = rag.query(query)

            # Verify result
            assert result == expected_completion

            # Verify Complete was called with correct prompt if context exists
            if context:
                mock_complete.assert_called_once()
                call_args = mock_complete.call_args[0]
                assert "mistral-large2" in call_args
                assert query in call_args[1]
                assert all(c in call_args[1] for c in context)
            else:
                mock_complete.assert_called_once()


def test_rag_from_scratch_retrieve_context(mock_rag_dependencies):
    """Test RAG_from_scratch retrieve_context method."""
    expected_results = ["result1", "result2"]

    rag = RAG_from_scratch()

    # Mock retriever's retrieve method
    with patch.object(rag.retriever, "retrieve", return_value=expected_results) as mock_retrieve:
        results = rag.retrieve_context("test query")

        # Verify results
        assert results == expected_results
        mock_retrieve.assert_called_once_with("test query")


def test_rag_from_scratch_generate_completion(mock_rag_dependencies):
    """Test RAG_from_scratch generate_completion method."""
    query = "test query"
    context = ["context1", "context2"]
    expected_completion = "test completion"

    rag = RAG_from_scratch()

    with patch("evaluate_cortex.Complete", return_value=expected_completion) as mock_complete:
        result = rag.generate_completion(query, context)

        # Verify result
        assert result == expected_completion

        # Verify Complete was called with correct prompt
        mock_complete.assert_called_once()
        call_args = mock_complete.call_args[0]
        assert "mistral-large2" in call_args
        assert query in call_args[1]
        assert all(c in call_args[1] for c in context)

"""
Shared test configuration and fixtures.
"""
import os

import pytest
from dotenv import load_dotenv


@pytest.fixture(autouse=True)
def load_env():
    """Load environment variables before each test."""
    load_dotenv()

    # Verify required environment variables are set
    required_vars = [
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_USER_PASSWORD",
        "SNOWFLAKE_ROLE",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_CORTEX_SEARCH_SERVICE",
    ]

    for var in required_vars:
        assert os.getenv(var) is not None, f"Environment variable {var} is not set"

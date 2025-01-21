"""
Cortex Search Service Evaluator using TruLens.
This script evaluates context relevance for EDU_SERVICE.
"""
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from snowflake.core import Root
from snowflake.cortex import Complete
from snowflake.snowpark.session import Session
from trulens.apps.custom import TruCustomApp, instrument
from trulens.connectors.snowflake import SnowflakeConnector
from trulens.core import Feedback, Select, TruSession
from trulens.providers.cortex.provider import Cortex

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Connection parameters
connection_params = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_USER_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
}

# Global variables for TruLens
tru_snowflake_connector = None
tru_session = None


def initialize_trulens(snowpark_session: Session) -> None:
    """Initialize global TruLens connector and session."""
    global tru_snowflake_connector, tru_session
    tru_snowflake_connector = SnowflakeConnector(snowpark_session=snowpark_session)
    tru_session = TruSession(connector=tru_snowflake_connector)


class CortexSearchRetriever:
    """Retriever class for Cortex search service."""

    def __init__(self, snowpark_session: Session, limit_to_retrieve: int = 4):
        """Initialize with Snowpark session and retrieval limit."""
        self._snowpark_session = snowpark_session
        self._limit_to_retrieve = limit_to_retrieve

    def retrieve(self, query: str) -> List[str]:
        """
        Retrieve relevant documents using Cortex search service.

        Args:
            query: Search query string

        Returns:
            List of retrieved document texts
        """
        try:
            cortex_search_service = (
                Root()
                .databases[os.getenv("SNOWFLAKE_DATABASE")]
                .schemas[os.getenv("SNOWFLAKE_SCHEMA")]
                .cortex_search_services[os.getenv("SNOWFLAKE_CORTEX_SEARCH_SERVICE")]
            )

            logger.info(f"Searching with query: {query}")
            resp = cortex_search_service.search(
                query=query,
                columns=["CHUNK"],
                limit=self._limit_to_retrieve,
            )

            if resp and hasattr(resp, "results"):
                return [curr["CHUNK"] for curr in resp.results]
            else:
                logger.warning("No results found or invalid response format")
                return []

        except Exception as e:
            logger.error(f"Error during retrieval: {str(e)}")
            return []


def create_snowpark_session():
    try:
        logger.info("Creating Snowpark session...")
        snowpark_session = Session.builder.configs(connection_params).create()
        logger.info("Successfully created Snowpark session")
        return snowpark_session
    except Exception as e:
        logger.error(f"Error creating Snowpark session: {str(e)}")
        return None


class RAG_from_scratch:
    def __init__(self):
        """Initialize RAG with Cortex search."""
        snowpark_session = create_snowpark_session()
        initialize_trulens(snowpark_session)
        self.retriever = CortexSearchRetriever(snowpark_session=snowpark_session, limit_to_retrieve=4)
        self.tru_snowflake_connector = tru_snowflake_connector
        self.tru_session = tru_session

    @instrument
    def retrieve_context(self, query: str) -> List[str]:
        """
        Retrieve relevant text from vector store.

        Args:
            query: The search query

        Returns:
            List of relevant text snippets
        """
        return self.retriever.retrieve(query)

    @instrument
    def generate_completion(self, query: str, context: List[str]) -> str:
        """Generate a completion using the LLM."""
        prompt = f"""
          You are an expert assistant extracting information from context provided.
          Answer the question based on the context. Be concise and do not hallucinate.
          If you don´t have the information just say so.
          Context: {context}
          Question:
          {query}
          Answer:
        """
        result = Complete("mistral-large2", prompt)
        return str(result) if result is not None else ""

    @instrument
    def query(self, query: str) -> str:
        """Process a query through the RAG pipeline."""
        context = self.retrieve_context(query)
        result = self.generate_completion(query, context)
        return str(result) if result is not None else ""


def main():
    """Main function to test the Cortex search retriever."""
    try:
        snowpark_session = create_snowpark_session()

        # Initialize retriever
        retriever = CortexSearchRetriever(snowpark_session=snowpark_session)

        # Test queries
        test_queries = [
            "What is financial literacy?",
            "What are the key factors in financial literacy?",
            "What are the benefits of financial literacy?",
        ]

        # Test retrieval
        for query in test_queries:
            logger.info(f"\nTesting query: {query}")
            results = retriever.retrieve(query)

            if results:
                logger.info(f"Found {len(results)} results:")
                for i, doc in enumerate(results, 1):
                    logger.info(f"\nResult {i}:")
                    logger.info(f"{doc[:200]}...")
            else:
                logger.warning("No results found")

        logger.info("\nTest complete!")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        if "snowpark_session" in locals():
            snowpark_session.close()
            logger.info("Closed Snowpark session")


def feedback_function():
    """Evaluate search results using TruLens feedback."""
    try:
        snowpark_session = create_snowpark_session()
        # Fix: Pass snowpark_session instead of connection
        provider = Cortex(snowpark_session, "mistral-large2")
        initialize_trulens(snowpark_session)

        f_groundedness = (
            Feedback(provider.groundedness_measure_with_cot_reasons, name="Groundedness")
            .on(Select.RecordCalls.retrieve_context.rets[:].collect())
            .on_output()
        )

        f_context_relevance = (
            Feedback(provider.context_relevance, name="Context Relevance")
            .on_input()
            .on(Select.RecordCalls.retrieve_context.rets[:])
            .aggregate(np.mean)
        )

        f_answer_relevance = Feedback(provider.relevance, name="Answer Relevance").on_input().on_output().aggregate(np.mean)
    except Exception as e:
        logger.error(f"Error in feedback_function: {str(e)}")
    finally:
        if "snowpark_session" in locals():
            snowpark_session.close()
            logger.info("Closed Snowpark session")


def convert_to_serializable(obj):
    """Convert objects to JSON serializable format."""
    if isinstance(obj, (pd.Series, pd.DataFrame)):
        return obj.to_dict()
    elif isinstance(obj, (np.int64, np.float64)):
        return int(obj) if isinstance(obj, np.int64) else float(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, tuple):
        return list(obj)  # Convert tuples to lists
    return obj


def save_query_results(prompts_and_responses, filename="query_results.csv"):
    """Save query results to a CSV file."""
    try:
        df = pd.DataFrame(prompts_and_responses)
        df["timestamp"] = datetime.now()
        df.to_csv(filename, index=False)
        logger.info(f"Query results saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving query results: {str(e)}")


def save_evaluation_results(results, output_prefix):
    """Save evaluation results to JSON files."""
    try:
        # Process metrics for time series data
        metrics_data = {}
        for k, v in results.items():
            if isinstance(k, tuple):
                k = "_".join(str(i) for i in k)  # Convert tuple keys to string
            metrics_data[str(k)] = convert_to_serializable(v)

        # Save metrics data
        metrics_file = f"{output_prefix}_metrics.json"
        with open(metrics_file, "w") as f:
            json.dump(metrics_data, f, indent=2, default=convert_to_serializable)
        logger.info(f"Saved metrics data to {metrics_file}")

    except Exception as e:
        logger.error(f"Error saving evaluation results: {str(e)}")
        raise


def save_evaluation_results_detailed(evaluation_results, filename="evaluation_results_detailed.csv"):
    """Save evaluation results to a CSV file."""
    try:
        # Convert evaluation results to a proper format for DataFrame
        formatted_results = []
        for result in evaluation_results:
            formatted_result = {
                "Service": result.get("service", "EDU_SERVICE"),
                "Query": result.get("query", ""),
                "Groundedness": float(result.get("groundedness", 0)),
                "Context_Relevance": float(result.get("context_relevance", 0)),
                "Answer_Relevance": float(result.get("answer_relevance", 0)),
                "Response_Length": len(result.get("response", "")),
                "Context_Length": len(str(result.get("context", ""))),
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Latency": float(result.get("latency", 0)),
                "Total_Cost": float(result.get("total_cost", 0)),
            }
            formatted_results.append(formatted_result)

        df = pd.DataFrame(formatted_results)
        df.to_csv(filename, index=False)
        logger.info(f"Evaluation results saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving evaluation results: {str(e)}")


if __name__ == "__main__":
    main()
    rag = RAG_from_scratch()

    feedback_function()

    # Define prompts list
    prompts = [
        "What is financial literacy?",
        "what are the key factors in financial literacy?",
    ]

    # Initialize results storage
    all_results: Dict[str, List] = {
        "timestamps": [],
        "queries": [],
        "responses": [],
        "latencies": [],
        "costs": [],
        "groundedness_scores": [],
        "context_relevance_scores": [],
        "answer_relevance_scores": [],
    }

    # Process each prompt
    for prompt in prompts:
        start_time = time.time()

        # Get response from RAG
        response = rag.query(prompt)

        # Calculate metrics
        latency = time.time() - start_time

        # Store results
        timestamp = datetime.now().isoformat()
        all_results["timestamps"].append(timestamp)
        all_results["queries"].append(prompt)
        all_results["responses"].append(response)
        all_results["latencies"].append(latency)

        # Default values for metrics
        all_results["groundedness_scores"].append(0.0)
        all_results["context_relevance_scores"].append(0.0)
        all_results["answer_relevance_scores"].append(0.0)
        all_results["costs"].append(0.0)

        # Get TruLens feedback if available
        if tru_session:
            try:
                feedback = tru_session.get_records_and_feedback()
                if feedback and len(feedback) > 0:
                    latest_feedback = feedback[-1]
                    if isinstance(latest_feedback, dict):
                        metrics = latest_feedback.get("metrics", {})
                        all_results["groundedness_scores"][-1] = float(metrics.get("groundedness", 0.0))
                        all_results["context_relevance_scores"][-1] = float(metrics.get("context_relevance", 0.0))
                        all_results["answer_relevance_scores"][-1] = float(metrics.get("answer_relevance", 0.0))
                        all_results["costs"][-1] = float(metrics.get("total_cost", 0.0))
            except Exception as e:
                logger.error(f"Error processing feedback: {str(e)}")

    # Save results
    if all_results:
        save_evaluation_results(all_results, "cortex_evaluation_results")

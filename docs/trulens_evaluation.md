# TrueLens Integration Documentation



This document outlines how TrueLens is integrated into our application for evaluating Cortex Search Service performance.



## Overview



TrueLens is used to evaluate the quality and performance of our Cortex-based search and retrieval system. The integration is primarily handled through two main components:



1.  `evaluate_cortex.py`: Core evaluation logic

2.  `evaluation_dashboard.py`: Visualization of evaluation results



## Components



### 1. TrueLens Setup and Initialization



```python

from trulens.apps.custom import TruCustomApp, instrument

from trulens.connectors.snowflake import SnowflakeConnector

from trulens.core import Feedback, Select, TruSession

from trulens.providers.cortex.provider import Cortex



# Global TruLens instances

tru_snowflake_connector = None

tru_session = None



def initialize_trulens(snowpark_session: Session) -> None:

global tru_snowflake_connector, tru_session

tru_snowflake_connector = SnowflakeConnector(snowpark_session=snowpark_session)

tru_session = TruSession(connector=tru_snowflake_connector)

```



### 2. Cortex Search Evaluation



The `CortexSearchRetriever` class is instrumented with TruLens for evaluation:



```python

class CortexSearchRetriever:

def __init__(self, snowpark_session: Session, limit_to_retrieve: int = 4):

self._snowpark_session = snowpark_session

self._limit_to_retrieve = limit_to_retrieve



@instrument

def retrieve(self, query: str):

# Retrieval logic instrumented by TruLens

```



### 3. RAG Pipeline Integration



The RAG (Retrieval-Augmented Generation) pipeline is integrated with TruLens for end-to-end evaluation:



```python

class RAG_from_scratch:

def __init__(self):

snowpark_session = create_snowpark_session()

initialize_trulens(snowpark_session)

self.retriever = CortexSearchRetriever(snowpark_session=snowpark_session)

self.tru_snowflake_connector = tru_snowflake_connector

self.tru_session = tru_session

```



### 4. Evaluation Metrics



The following metrics are collected and evaluated:



1. Query Latency

2. Retrieval Cost

3. Groundedness Scores

4. Context Relevance



### 5. Dashboard Visualization



The evaluation dashboard (`evaluation_dashboard.py`) displays:



```python

# Key Metrics

- Total Queries

- Average Latency

- Total Cost



# Performance Visualizations

- Query Latency Over Time

- Groundedness Scores Trend

- Context Relevance Distribution

```



## Usage



1.  **Initialize Evaluation:**

```python

rag = RAG_from_scratch()

```



2.  **Run Evaluations:**

```python

results = rag.query("your search query")

```



3.  **View Results:**

```bash

streamlit run evaluation_dashboard.py

```



## Data Storage



Evaluation results are saved in multiple formats:



1.  `cortex_evaluation_results_metrics.json`: Core metrics

2.  `evaluation_results_detailed.csv`: Detailed evaluation data

3.  `query_results.csv`: Raw query results



## Current Limitations



1. Requires Snowflake connection parameters in environment variables

2. Limited to 4 retrieved documents per query by default

3. Dashboard requires local file access for metrics



## Best Practices



1. Always initialize TruLens before running evaluations

2. Use environment variables for sensitive credentials

3. Regular monitoring of evaluation metrics

4. Periodic review of groundedness scores

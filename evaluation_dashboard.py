import json

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Cortex Evaluation Dashboard", layout="wide")

st.title("Cortex Search Evaluation Dashboard")


# Load evaluation metrics
@st.cache_data
def load_metrics():
    try:
        with open("cortex_evaluation_results_metrics.json", "r") as f:
            data = json.load(f)
            return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


# Load the data
df = load_metrics()

if df is not None:
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Queries", len(df))

    with col2:
        avg_latency = df["latencies"].mean() if "latencies" in df else 0
        st.metric("Average Latency", f"{avg_latency:.2f}s")

    with col3:
        total_cost = df["costs"].sum() if "costs" in df else 0
        st.metric("Total Cost", f"${total_cost:.4f}")

    # Create time series plots
    st.subheader("Performance Metrics Over Time")

    if "latencies" in df:
        fig_latency = px.line(df, x=df.index, y="latencies", title="Query Latency")
        st.plotly_chart(fig_latency)

    if "groundedness_scores" in df:
        fig_quality = px.line(
            df,
            x=df.index,
            y=[
                "groundedness_scores",
                "context_relevance_scores",
                "answer_relevance_scores",
            ],
            title="Quality Metrics",
        )
        st.plotly_chart(fig_quality)

    # Show query details
    st.subheader("Query Details")
    if "queries" in df and "responses" in df:
        for i, (query, response) in enumerate(zip(df["queries"], df["responses"])):
            with st.expander(f"Query {i+1}: {query}"):
                st.write("Response:", response)
                if "groundedness_scores" in df:
                    st.write(f"Groundedness: {df['groundedness_scores'].iloc[i]:.2f}")
                if "context_relevance_scores" in df:
                    st.write(f"Context Relevance: {df['context_relevance_scores'].iloc[i]:.2f}")
                if "answer_relevance_scores" in df:
                    st.write(f"Answer Relevance: {df['answer_relevance_scores'].iloc[i]:.2f}")

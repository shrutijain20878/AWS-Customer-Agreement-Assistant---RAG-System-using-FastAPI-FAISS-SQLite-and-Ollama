import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AWS Customer Agreement Assistant",
    layout="wide"
)

st.title("AWS Customer Agreement Assistant")
st.caption(
    "Retrieval-Augmented Generation (RAG) System using FastAPI, FAISS, SQLite and Ollama"
)

# Sidebar
with st.sidebar:

    st.header("System Status")

    try:

        health = requests.get(
            f"{BACKEND_URL}/health"
        )

        if health.status_code == 200:

            status = health.json()

            st.success(
                f"Backend: {status['status']}"
            )

            st.write(
                f"Document Loaded: {status['document_loaded']}"
            )

    except Exception:

        st.error(
            "FastAPI backend is not running."
        )

    st.divider()

    st.subheader("Document Management")

    if st.button("Ingest AWS Agreement"):

        with st.spinner(
            "Processing PDF..."
        ):

            response = requests.post(
                f"{BACKEND_URL}/ingest"
            )

            if response.status_code == 200:

                data = response.json()

                st.success(
                    f"Document processed successfully. "
                    f"{data['chunks_created']} chunks created."
                )

            else:

                st.error(
                    response.text
                )

# Tabs

chat_tab, analytics_tab = st.tabs(
    [
        "Chat Assistant",
        "Analytics Dashboard"
    ]
)

# Chat Tab
with chat_tab:

    st.subheader(
        "Ask Questions About AWS Customer Agreement"
    )

    question = st.text_input(
        "Enter your question"
    )

    if st.button("Ask Question"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Generating answer..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "question": question
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    st.write(
                        data["answer"]
                    )

                    st.subheader(
                        "Retrieved Source Chunks from LLM"
                    )

                    for source in data["sources"]:
                        st.info(source)

                else:

                    st.error(
                        response.text
                    )
# Analytics Tab
with analytics_tab:

    st.subheader(
        "Usage Analytics Dashboard"
    )

    if st.button(
        "Load Analytics"
    ):

        response = requests.get(
            f"{BACKEND_URL}/analytics"
        )

        if response.status_code == 200:

            data = response.json()

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Average Latency (ms)",
                    data["average_latency_ms"]
                )

            with col2:

                st.metric(
                    "Success Rate (%)",
                    data["success_rate"]
                )

            with col3:

                st.metric(
                    "Total Queries",
                    data["total_queries"]
                )

            st.divider()

            st.subheader(
                "Most Frequently Asked Questions"
            )

            freq_questions = data[
                "most_frequent_questions"
            ]

            if freq_questions:

                freq_df = pd.DataFrame(
                    freq_questions
                )

                st.dataframe(
                    freq_df,
                    use_container_width=True
                )

                st.bar_chart(
                    freq_df.set_index(
                        "question"
                    )["count"]
                )

            else:

                st.info(
                    "No analytics data available."
                )

            st.divider()

            st.subheader(
                "Queries With No Answer Found"
            )

            no_answer_queries = data[
                "no_answer_queries"
            ]

            if no_answer_queries:

                no_answer_df = pd.DataFrame(
                    {
                        "Question":
                        no_answer_queries
                    }
                )

                st.dataframe(
                    no_answer_df,
                    use_container_width=True
                )

            else:

                st.success(
                    "All queries were answered."
                )

        else:

            st.error(
                response.text
            )
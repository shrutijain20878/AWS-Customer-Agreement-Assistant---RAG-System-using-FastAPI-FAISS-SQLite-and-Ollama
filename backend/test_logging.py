from logger import log_query

log_query(
    query="Can AWS suspend my account?",
    answer="Yes, AWS may suspend accounts.",
    answer_found=True,
    latency_ms=420,
    retrieved_chunks=3
)

print("Log inserted.")
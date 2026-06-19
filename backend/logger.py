from database import SessionLocal
from models import QueryLog


def log_query(
    query,
    answer,
    answer_found,
    latency_ms,
    retrieved_chunks
):

    db = SessionLocal()

    try:

        log = QueryLog(
            query=query,
            answer=answer,
            answer_found=answer_found,
            latency_ms=latency_ms,
            retrieved_chunks=retrieved_chunks
        )

        db.add(log)

        db.commit()

    finally:
        db.close()
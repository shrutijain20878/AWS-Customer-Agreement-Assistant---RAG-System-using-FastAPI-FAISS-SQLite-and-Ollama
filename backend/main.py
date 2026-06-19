from pathlib import Path
import time

from fastapi import FastAPI, HTTPException
from sqlalchemy import func

from schemas import (
    AskRequest,
    AskResponse,
    IngestResponse
)

from rag.pdf_parser import extract_text
from rag.chunker import create_chunks
from rag.embedder import generate_embeddings

from rag.vector_store import (
    save_vector_store,
    load_vector_store
)

from rag.retriever import retrieve
from rag.generator import generate_answer

from logger import log_query

from database import SessionLocal
from models import QueryLog

app = FastAPI(
    title="AWS Customer Agreement RAG API"
)

index = None
chunks = None

PDF_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "AWS Customer Agreement.pdf"
)


@app.on_event("startup")
def startup_event():

    global index
    global chunks

    try:
        index, chunks = load_vector_store()
        print("Vector Store Loaded")

    except Exception:
        print("No Vector Store Found")


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "document_loaded": index is not None
    }


@app.post(
    "/ingest",
    response_model=IngestResponse
)
def ingest_pdf():

    global index
    global chunks

    if not PDF_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF file not found."
        )

    text = extract_text(str(PDF_PATH))

    chunks = create_chunks(text)

    embeddings = generate_embeddings(chunks)

    save_vector_store(
        embeddings,
        chunks
    )

    index, chunks = load_vector_store()

    return {
        "message": "Document processed successfully",
        "chunks_created": len(chunks)
    }


@app.post(
    "/ask",
    response_model=AskResponse
)
def ask_question(request: AskRequest):

    global index
    global chunks

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    if index is None:
        raise HTTPException(
            status_code=400,
            detail="Document not ingested."
        )

    start_time = time.time()

    retrieved_chunks = retrieve(
        query=request.question,
        index=index,
        chunks=chunks,
        k=2
    )

    answer = generate_answer(
        request.question,
        retrieved_chunks
    )

    answer_found = (
        "NOT_FOUND" not in answer.upper()
    )

    if not answer_found:
        answer = (
            "The answer was not found "
            "in the AWS Customer Agreement."
        )

    latency_ms = (
        time.time() - start_time
    ) * 1000

    log_query(
        query=request.question,
        answer=answer,
        answer_found=answer_found,
        latency_ms=latency_ms,
        retrieved_chunks=len(retrieved_chunks)
    )

    return {
        "answer": answer,
        "sources": retrieved_chunks
    }


@app.get("/analytics")
def analytics():

    db = SessionLocal()

    try:

        avg_latency = db.query(
            func.avg(QueryLog.latency_ms)
        ).scalar()

        frequent_questions = (
            db.query(
                QueryLog.query,
                func.count(
                    QueryLog.query
                ).label("count")
            )
            .group_by(QueryLog.query)
            .order_by(
                func.count(
                    QueryLog.query
                ).desc()
            )
            .limit(5)
            .all()
        )

        no_answer_queries = (
            db.query(QueryLog.query)
            .filter(
                QueryLog.answer_found == False
            )
            .all()
        )

        total_queries = (
            db.query(QueryLog)
            .count()
        )

        successful_queries = (
            db.query(QueryLog)
            .filter(
                QueryLog.answer_found == True
            )
            .count()
        )

        success_rate = 0

        if total_queries > 0:
            success_rate = round(
                (
                    successful_queries
                    / total_queries
                ) * 100,
                2
            )

        return {
            "average_latency_ms": round(
                avg_latency or 0,
                2
            ),

            "success_rate": success_rate,

            "total_queries": total_queries,

            "most_frequent_questions": [
                {
                    "question": q,
                    "count": c
                }
                for q, c in frequent_questions
            ],

            "no_answer_queries": [
                q[0]
                for q in no_answer_queries
            ]
        }

    finally:
        db.close()
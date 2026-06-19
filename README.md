# AWS Customer Agreement RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for answering questions about the AWS Customer Agreement document.

The system processes the PDF, creates embeddings, stores them in a FAISS vector database, retrieves relevant document chunks for user questions, and generates responses using a local Large Language Model (LLM) through Ollama.

Additionally, all user interactions are logged into a SQLite database, enabling usage analytics through a FastAPI endpoint and a Streamlit dashboard.

---

## Features

### RAG Pipeline

* PDF parsing using PyPDF
* Text chunking with overlap
* Embedding generation using Sentence Transformers
* Vector search using FAISS
* Context-aware answer generation using Ollama (Llama 3)
* Source chunk retrieval
* No-answer detection to reduce hallucinations

### FastAPI Backend

* POST `/ingest`
* POST `/ask`
* GET `/analytics`
* GET `/health`

### SQL Analytics

Tracks:

* User query
* Generated answer
* Response latency
* Answer found status
* Retrieved chunk count
* Timestamp

Analytics include:

* Most frequently asked questions
* Queries where no answer was found
* Average response latency
* Success rate
* Total query count

### Streamlit Dashboard

* Chat-style question answering interface
* Source chunk display
* Analytics dashboard
* Charts and tables for usage insights

---

## Architecture

User Question

↓

Streamlit Frontend

↓

FastAPI Backend

↓

Retriever (FAISS)

↓

Relevant Chunks

↓

Ollama (Llama 3)

↓

Generated Answer

↓

SQLite Logging

↓

Analytics Dashboard

---

## Technology Stack

### Backend

* FastAPI
* Python

### RAG Components

* Sentence Transformers (`all-MiniLM-L6-v2`)
* FAISS
* Ollama
* Llama 3

### Database

* SQLite
* SQLAlchemy

### Frontend

* Streamlit

---

## Design Decisions

### Chunking Strategy

Chunk Size: 500 characters

Chunk Overlap: 50 characters

Reasoning:

* Smaller chunks improve retrieval precision.
* Overlap preserves context between adjacent chunks.
* Suitable for legal documents with section-based structure.

### Embedding Model

Model:

`all-MiniLM-L6-v2`

Reasoning:

* Lightweight
* Fast inference
* Good semantic retrieval performance
* Fully free and local

### Vector Store

FAISS was selected because:

* Lightweight
* No external hosting required
* Fast similarity search
* Suitable for assignment-scale datasets

### LLM

Model:

`llama3`

Provider:

Ollama

Reasoning:

* Runs locally
* No API cost
* Easy integration
* Strong instruction following

### Retrieval Strategy

Top-K Retrieval:

`k = 3`

Reasoning:

* Provides sufficient context
* Avoids prompt overload
* Reduces irrelevant information

### Hallucination Mitigation

The retriever applies a similarity threshold.

If no relevant chunks are retrieved, the system returns:

"The answer was not found in the AWS Customer Agreement."

instead of generating unsupported content.

---

## Database Schema

Table: query_logs

| Column           | Description                |
| ---------------- | -------------------------- |
| id               | Primary Key                |
| query            | User question              |
| answer           | Generated answer           |
| answer_found     | Boolean                    |
| latency_ms       | Response latency           |
| retrieved_chunks | Number of chunks retrieved |
| timestamp        | Query timestamp            |

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository_url>

cd aws_rag_assignment
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ollama

```bash
ollama serve
```

Verify model:

```bash
ollama list
```

Expected:

```bash
llama3
nomic-embed-text
```

### 5. Create Database

```bash
cd backend

python create_db.py
```

### 6. Start FastAPI

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

### 7. Start Streamlit

Open a new terminal:

```bash
cd frontend

streamlit run app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## API Endpoints

### POST /ingest

Processes the AWS Customer Agreement PDF and creates embeddings.

### POST /ask

Accepts a user question and returns:

* Answer
* Source chunks

### GET /analytics

Returns usage analytics.

### GET /health

Returns system health information.
---

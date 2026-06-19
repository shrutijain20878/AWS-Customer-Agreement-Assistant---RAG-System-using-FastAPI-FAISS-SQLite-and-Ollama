from pathlib import Path

from rag.pdf_parser import extract_text
from rag.chunker import create_chunks
from rag.embedder import generate_embeddings
from rag.vector_store import save_vector_store

pdf_path = (
    Path(__file__).parent.parent
    / "data"
    / "AWS Customer Agreement.pdf"
)

text = extract_text(str(pdf_path))

chunks = create_chunks(text)

print("Chunks:", len(chunks))

embeddings = generate_embeddings(chunks)

print("Embeddings Shape:", embeddings.shape)

save_vector_store(
    embeddings,
    chunks
)

print("FAISS index saved successfully.")
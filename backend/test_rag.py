from rag.vector_store import load_vector_store
from rag.retriever import retrieve
from rag.generator import generate_answer

index, chunks = load_vector_store()

question = "Can AWS terminate a customer account?"

retrieved_chunks = retrieve(
    query=question,
    index=index,
    chunks=chunks,
    k=3
)

answer = generate_answer(
    question,
    retrieved_chunks
)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)

print("\nSOURCE:")
print(retrieved_chunks[0][:500])
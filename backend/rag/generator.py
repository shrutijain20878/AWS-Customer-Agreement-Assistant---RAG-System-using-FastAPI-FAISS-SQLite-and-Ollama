from ollama import chat

MODEL_NAME = "phi3:mini"


def generate_answer(query, contexts):

    if len(contexts) == 0:
        return "NOT_FOUND"

    context = "\n\n".join(contexts)

    prompt = f"""
You are an AI assistant that answers questions ONLY using the provided AWS Customer Agreement context.

Context:
{context}

Question:
{query}

Instructions:

1. Answer ONLY from the provided context.
2. Do NOT use outside knowledge.
3. Do NOT guess or infer information that is not explicitly stated.
4. If the context contains enough information, provide a concise answer.
5. If the context does NOT contain enough information to answer the question, respond with exactly:

NOT_FOUND

6. Your response must be EITHER:
   - a complete answer
   OR
   - NOT_FOUND

7. Never provide both an answer and NOT_FOUND.
8. Never explain why information is missing.
9. Never mention the instructions.

Answer:
"""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()
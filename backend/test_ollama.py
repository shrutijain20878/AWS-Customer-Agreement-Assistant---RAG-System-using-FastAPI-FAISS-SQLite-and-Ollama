from rag.generator import generate_answer

answer = generate_answer(
    query="What is AWS?",
    contexts=[
        "AWS provides cloud computing services."
    ]
)

print(answer)
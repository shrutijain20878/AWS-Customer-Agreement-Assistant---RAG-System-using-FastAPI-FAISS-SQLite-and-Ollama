from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def retrieve(
    query,
    index,
    chunks,
    k=3
):

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(
        np.array(query_embedding),
        k
    )

    THRESHOLD = 1.5

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if distance < THRESHOLD:

            results.append(
                chunks[idx]
            )

    return results
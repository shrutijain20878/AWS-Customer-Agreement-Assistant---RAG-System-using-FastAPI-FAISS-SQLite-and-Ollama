import faiss
import pickle
import numpy as np
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# vector_store folder
VECTOR_DIR = BASE_DIR / "vector_store"

# create folder if it doesn't exist
VECTOR_DIR.mkdir(exist_ok=True)

INDEX_PATH = str(VECTOR_DIR / "faiss.index")
CHUNKS_PATH = str(VECTOR_DIR / "chunks.pkl")


def save_vector_store(embeddings, chunks):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    faiss.write_index(index, INDEX_PATH)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)


def load_vector_store():

    index = faiss.read_index(INDEX_PATH)

    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks
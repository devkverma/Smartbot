import faiss
import numpy as np


class Database:

    def __init__(self, embeddings):
        self.dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dim)
        self.index.add(embeddings)

    def retrieve(self, query, chunk_lookup):
        distance, indices = self.index.search(query, k=5)

        return [chunk_lookup[i].text for i in indices[0]]
    
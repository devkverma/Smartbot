from sentence_transformers import SentenceTransformer

class Embed_Agent:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embed_dim = self.model.get_sentence_embedding_dimension()

    def embed_chunks(self, documents):
        texts = []
        chunk_lookup = []

        for doc in documents:
            for chunk in doc.chunks:
                texts.append(chunk.text)
                chunk_lookup.append(chunk)
        
        embeddings = self.model.encode(
            texts,
            batch_size = 32,
            show_progress_bar = True,
            normalize_embeddings=True,
        )

        return embeddings, chunk_lookup
    
    def embed_query(self, query):
        return self.model.encode(
            [query],
            normalize_embeddings=True
        )
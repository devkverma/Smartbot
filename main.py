from src.chunking.chunk_document import create_data
from src.embeddings.create_embeddings import Model
from src.database.vector_database import Database
import sys

if __name__ == "__main__":
    path = "./data/raw"

    Data = create_data(path)

    model = Model()

    embeddings, chunk_lookup = model.embed_chunks(Data)
    database = Database(embeddings)

    while True:
        user = input("\nYou: ")
        if (user.lower() == "exit"):
            break   

        query = user
        query = model.embed_query(query)
        source = database.retrieve(query, chunk_lookup)[0]
        sys.stdout.write(f"source: {source}\n")
        sys.stdout.flush()
    sys.stdout.write("Exiting program...")

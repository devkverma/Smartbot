from src.chunking.chunk_document import create_data
from src.embeddings.create_embeddings import Embed_Agent
from src.database.vector_database import Database
from src.model.mistral import Model
from models import ensure_model
import sys
import os

if __name__ == "__main__":
    path = "./data/raw"
    ensure_model()
    Data = create_data(path)

    embed_agent = Embed_Agent()

    embeddings, chunk_lookup = embed_agent.embed_chunks(Data)
    database = Database(embeddings)

    model = Model()

    while True:
        user = input("\nYou: ")
        if (user.lower() == "/exit"):
            break

        if (user.lower() == "/clear"):
            os.system("cls" if os.name == "nt" else "clear")
            continue

        query = embed_agent.embed_query(user)
        retrieved_chunks = database.retrieve(query, chunk_lookup, top_k=3)
        
        prompt = model.build_prompt(retrieved_chunks, user)
        answer = model.ask_model(prompt)

    sys.stdout.write("Exiting program...")

from src.chunking.chunk_document import create_data

path = "./data/raw"

Data = create_data(path)

for doc in Data:
    print(doc.name)

    # for chunk in doc.chunks:
    #     print(f"{chunk.chunk_index} -- {chunk.chunk_id}: {chunk.text[:20]}")
from dataclasses import dataclass, field, asdict
import json
import uuid
from pypdf import PdfReader
import os
from typing import List
import sys
from assets.loading_animations import Animation
import threading

@dataclass
class Document:
    doc_id: str
    name: str
    location: str
    chunks: List["Chunk"] = field(default_factory=list)
    total_chunks: int = 0
     
    

@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    chunk_index: int
    tokens: int
    text: str


animation = Animation()

def tokenise(text):
    return text.split()

def chunk_text(document: Document, max_tokens = 500, overlap = 100):
    sys.stdout.write(f"\n{document.name}\n")
    reader =PdfReader(os.path.join(document.location, document.name))
    chunks = []
    index = 0
    pages = reader.pages
    hasContent = True
    for i, page in enumerate(pages): 
        animation.progress_bar(i, len(pages))
        text = page.extract_text()
        if not text or not text.strip():
            hasContent = False
            continue
        hasContent = True
        tokens = tokenise(text)
        start = 0
        
        while start < len(tokens):
            end = start + max_tokens
            window = tokens[start:end]

            chunk_text = " ".join(window)

            chunk = Chunk(
                chunk_id=f"chunk_{uuid.uuid4()}",
                doc_id=document.doc_id,
                chunk_index=index,
                tokens=len(window),
                text=chunk_text
            )

            chunks.append(chunk)
            index += 1
            start += max_tokens - overlap
    if not hasContent:
        sys.stdout.write(f"\nCouldn't read {document.name}\n")
        sys.stdout.flush()
        return []
    animation.progress_bar(100,100)
    sys.stdout.write("\n")
    sys.stdout.flush()
    document.total_chunks = len(chunks)
    return chunks


def create_data(path):
    pdfs = [f for f in os.listdir(path) if f != 'upload_files_here.txt']
    if not pdfs:
        sys.stdout.write("No pdfs uploaded! Running model without knowledge base.\n")
        sys.stdout.flush()
        return None
    
    data = clean_metadata(path)
    existing_files = {doc.name for doc in data}

    files = [f for f in os.listdir(path) if f.lower().endswith(".pdf")]

    for file in files:
        if file in existing_files:
            continue

        doc = Document(
            doc_id=str(uuid.uuid4()),
            name=file,
            location=path
        )
        chunks = chunk_text(doc)
        if not chunks:
            continue
        doc.chunks = chunks
        data.append(doc)

    save_metadata(data)
    if pdfs:
        sys.stdout.write("\rMetadata was loaded successfully... ✅\n")
    return data



def save_metadata(data: List[Document], output_file="metadata.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            [asdict(doc) for doc in data],
            f,
            indent=4,
            ensure_ascii=False
        )

def load_metadata(file="metadata.json"):
    sys.stdout.write("\rLoading metadata...")
    if not os.path.exists(file):
        sys.stdout.write("\rMetadata not found. Creating one...")
        return []

    with open(file, "r", encoding="utf-8") as f:
        raw = json.load(f)

    documents = []
    for d in raw:
        chunks = [Chunk(**c) for c in d.get("chunks", [])]
        documents.append(
            Document(
                doc_id=d["doc_id"],
                name=d["name"],
                location=d["location"],
                chunks=chunks,
                total_chunks=d.get("total_chunks", len(chunks))
            )
        )
    return documents

def clean_metadata(path, metadata_file="metadata.json"):
    current_files = {
        f for f in os.listdir(path) if f.lower().endswith(".pdf")
    }

    data = load_metadata(metadata_file)

    cleaned_data = [doc for doc in data if doc.name in current_files and doc.chunks]

    if len(cleaned_data) == len(data):
        return data

    save_metadata(cleaned_data, metadata_file)
    return cleaned_data
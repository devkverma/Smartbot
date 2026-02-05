# SmartBot — Your Local RAG LLM

This is a personal hobby project exploring how Retrieval-Augmented Generation (RAG) systems work when run fully locally.

The goal is to build a practical, offline document assistant powered by a local LLM, without relying on external APIs.

## What it does

* Reads local PDF documents
* Splits them into meaningful chunks (custom chunking implementation)
* Converts text into embeddings using SentenceTransformers
* Stores and searches embeddings using FAISS
* Retrieves relevant context for a query
* Uses a local Mistral model (via llama.cpp) to generate grounded answers

The entire pipeline runs locally after setup.

## Tech used

* FAISS for vector database
* SentenceTransformers for embeddings
* Custom document chunking logic
* llama-cpp-python for local LLM inference
* Mistral GGUF model

## Running the project

A `main.bat` script is included to:

* activate the virtual environment
* launch the application

No manual environment setup needed after initial installation.

## Learning focus

This project exists to understand:

* how RAG pipelines work internally
* how embeddings and retrieval affect answer quality
* how local LLM inference behaves vs hosted models
* tradeoffs between latency, accuracy, and memory

## Possible future additions

* OCR support for scanned PDFs
* ANN optimization for faster retrieval
* hybrid search (BM25 + embeddings)
* reranking using cross-encoders
* metadata-aware retrieval
* streaming over a web interface
* evaluation pipeline for answer accuracy
* incremental indexing for new documents
* multi-document citation support


"""
Ingestion pipeline: chunks scraped content, generates embeddings
using Google's free embedding API, and builds a FAISS index.

Usage:
    python3 ingest.py

Prerequisites:
    - Run scraper.py first to generate data/pages.json
    - Set GOOGLE_API_KEY in your .env file
"""

import os
import json
import time
import numpy as np
import faiss
import google.generativeai as genai
from dotenv import load_dotenv
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def chunk_text(text, url, title):
    """
    Split text into overlapping chunks of roughly CHUNK_SIZE words.
    Each chunk keeps metadata (source URL and title) so we can
    cite sources in chatbot responses later.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + CHUNK_SIZE
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        chunks.append({
            "text": chunk_text,
            "url": url,
            "title": title,
            "word_count": len(chunk_words),
        })

        # Move forward by (CHUNK_SIZE - CHUNK_OVERLAP) words
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def generate_embeddings(texts, batch_size=5):
    """
    Generate embeddings for a list of texts using Google's free API.
    Processes in batches to respect rate limits.
    """
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        print(f"  Embedding batch {i // batch_size + 1}"
              f"/{(len(texts) - 1) // batch_size + 1}...")

        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=batch,
            task_type="retrieval_document",
        )
        all_embeddings.extend(result["embedding"])

        # Wait between batches to avoid rate limits
        time.sleep(5)

    return np.array(all_embeddings, dtype=np.float32)


def build_index(embeddings):
    """
    Build a FAISS index using inner product (cosine similarity).
    Normalises vectors first so inner product == cosine similarity.
    """
    # Normalise so inner product equals cosine similarity
    faiss.normalize_L2(embeddings)

    # Create index - IndexFlatIP = exact inner product search
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index


def main():
    """Run the full ingestion pipeline."""
    print("=" * 60)
    print("Content Ingestion Pipeline")
    print("=" * 60)

    # Load scraped pages
    pages_path = os.path.join("data", "pages.json")
    if not os.path.exists(pages_path):
        print("Error: data/pages.json not found. Run scraper.py first.")
        return

    with open(pages_path, "r", encoding="utf-8") as f:
        pages = json.load(f)

    print(f"Loaded {len(pages)} pages\n")

    # Step 1: Chunk all pages
    print("Step 1: Chunking content...")
    all_chunks = []
    for page in pages:
        chunks = chunk_text(page["content"], page["url"], page["title"])
        all_chunks.extend(chunks)
    print(f"  Created {len(all_chunks)} chunks\n")

    # Step 2: Generate embeddings
    print("Step 2: Generating embeddings...")
    texts = [chunk["text"] for chunk in all_chunks]
    embeddings = generate_embeddings(texts)
    print(f"  Embedding dimension: {embeddings.shape[1]}\n")

    # Step 3: Build FAISS index
    print("Step 3: Building FAISS index...")
    index = build_index(embeddings)
    print(f"  Index size: {index.ntotal} vectors\n")

    # Save index and chunks to disk
    os.makedirs("index", exist_ok=True)

    index_path = os.path.join("index", "kent.index")
    faiss.write_index(index, index_path)
    print(f"  Saved index to: {index_path}")

    chunks_path = os.path.join("index", "chunks.json")
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    print(f"  Saved chunks to: {chunks_path}")

    print(f"\nDone! Index ready with {len(all_chunks)} chunks.")


if __name__ == "__main__":
    main()

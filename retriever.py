"""
Retriever module: loads the FAISS index and performs similarity search
to find the most relevant content chunks for a given query.
"""

import os
import json
import time
import numpy as np
import faiss
import google.generativeai as genai
from config import TOP_K, EMBEDDING_MODEL


class Retriever:
    """Handles loading the FAISS index and retrieving relevant chunks."""

    def __init__(self, index_dir="index"):
        """Load the FAISS index and chunk metadata from disk."""
        index_path = os.path.join(index_dir, "kent.index")
        chunks_path = os.path.join(index_dir, "chunks.json")

        if not os.path.exists(index_path):
            raise FileNotFoundError(
                f"FAISS index not found at {index_path}. Run ingest.py first."
            )

        self.index = faiss.read_index(index_path)

        with open(chunks_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        print(f"Retriever loaded: {self.index.ntotal} chunks indexed")

    def embed_query(self, query):
        """Generate an embedding for the user's query."""
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=query,
            task_type="retrieval_query",
        )
        embedding = np.array([result["embedding"]], dtype=np.float32)
        faiss.normalize_L2(embedding)
        return embedding

    def retrieve(self, query, top_k=TOP_K):
        """
        Find the top-k most relevant chunks for a query.
        Returns a list of chunk dicts with text, url, title, and score.
        """
        query_embedding = self.embed_query(query)
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.chunks):
                chunk = self.chunks[idx].copy()
                chunk["score"] = float(score)
                results.append(chunk)

        return results

    def format_context(self, results):
        """
        Format retrieved chunks into a context string for the LLM prompt.
        Includes source attribution for each chunk.
        """
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Source {i}: {result['title']}]\n"
                f"{result['text']}\n"
                f"(URL: {result['url']})"
            )

        return "\n\n---\n\n".join(context_parts)

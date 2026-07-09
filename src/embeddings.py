# src/embeddings.py
# ─────────────────────────────────────────────────────────────────────────────
# Computes Google text embeddings for each graph node and stores them as
# node properties. These embeddings power the vector search step in the
# GraphRAG pipeline — when a user asks a question, we embed the question
# and find the graph nodes most semantically similar to it.
# ─────────────────────────────────────────────────────────────────────────────

import os
import json
import time
import numpy as np
from google import genai
from dotenv import load_dotenv
try:
    from db import Neo4jConnection
except ModuleNotFoundError:
    from src.db import Neo4jConnection

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
EMBED_MODEL = "gemini-embedding-001"


# ─────────────────────────────────────────────────────────────────────────────
# Node → Natural Language Description
# ─────────────────────────────────────────────────────────────────────────────

def node_to_text(props: dict, label: str) -> str:
    """
    Convert a graph node into a natural language sentence for embedding.

    The sentence should capture the node's most distinguishing properties so
    that a question about this entity will match it via cosine similarity.
    """
    if label == "Movie":
        return (
            f"'{props.get('title')}' is a {props.get('genre', '')} English film "
            f"released in {props.get('year', '')}. "
            f"{props.get('description', '')}"
        )
    if label == "Person":
        return (
            f"{props.get('name')} is an actor, director, or composer "
            f"born in {props.get('born', '')} from {props.get('hometown', '')}."
        )
    if label == "ProductionHouse":
        return (
            f"{props.get('name')} is a film production company founded in "
            f"{props.get('founded', '')} by {props.get('founder', 'unknown')}."
        )
    if label == "Award":
        return (
            f"The {props.get('name')} is a {props.get('category', '')} award "
            f"presented in {props.get('year', '')} in Hollywood/English cinema."
        )
    return props.get("name", props.get("title", str(props)))


# ─────────────────────────────────────────────────────────────────────────────
# Batch Embedding
# ─────────────────────────────────────────────────────────────────────────────

def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Call the Google Embeddings API for a list of texts.
    
    Includes chunking to handle batch size limits, and robust retries
    with exponential backoff to handle free-tier rate limits (429).
    """
    if not texts:
        return []

    # Chunking texts to handle free-tier limits and small batches.
    chunk_size = 25
    all_vectors = []
    
    for i in range(0, len(texts), chunk_size):
        chunk = texts[i:i + chunk_size]
        retries = 6
        delay = 5.0
        while retries > 0:
            try:
                response = client.models.embed_content(model=EMBED_MODEL, contents=chunk)
                chunk_vectors = [item.values for item in response.embeddings]
                all_vectors.extend(chunk_vectors)
                
                # Sleep briefly between chunks
                if i + chunk_size < len(texts):
                    time.sleep(1.0)
                break
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
                    if retries > 1:
                        print(f"  [Rate Limit] 429 resource exhausted. Retrying chunk in {delay:.1f}s... (Retries left: {retries - 1})")
                        time.sleep(delay)
                        delay *= 2
                        retries -= 1
                    else:
                        raise e
                else:
                    raise e
        else:
            raise RuntimeError("Failed to embed chunk due to persistent rate limits.")
            
    return all_vectors


def add_embeddings(db: Neo4jConnection) -> None:
    """
    Embed every node in the graph and store the vector as a JSON string property.

    Why JSON string? Neo4j Community Edition does not natively index float
    arrays as vectors. We store as JSON and deserialise in Python for
    similarity computation. For production scale, upgrade to Neo4j Enterprise
    which supports native vector indexes and GPU-accelerated ANN search.
    """
    labels = ["Movie", "Person", "ProductionHouse", "Award"]

    for label in labels:
        # Only fetch nodes that don't have embeddings to make this script resumable
        rows = db.read(f"MATCH (n:{label}) WHERE n.embedding IS NULL RETURN n, elementId(n) AS nid")
        if not rows:
            print(f"  ✓   0 {label} nodes embedded (all up to date)")
            continue

        # Process in sub-batches to keep the DB connection active and write incrementally
        sub_batch_size = 50
        total_embedded = 0
        
        for i in range(0, len(rows), sub_batch_size):
            chunk = rows[i: i + sub_batch_size]
            texts   = [node_to_text(row["n"], label) for row in chunk]
            nids    = [row["nid"] for row in chunk]
            vectors = embed_batch(texts)

            # Batch-write nodes using UNWIND to optimize DB performance
            batch_data = [{"nid": nid, "vec": json.dumps(vec), "txt": txt} for nid, vec, txt in zip(nids, vectors, texts)]
            if batch_data:
                db.write_batch("""
                    UNWIND $rows AS row
                    MATCH (n) WHERE elementId(n) = row.nid
                    SET n.embedding      = row.vec,
                        n.embedding_text = row.txt
                """, batch_data)
            
            total_embedded += len(chunk)

        print(f"  ✓ {total_embedded:>3} {label} nodes embedded")


# ─────────────────────────────────────────────────────────────────────────────
# Similarity Search
# ─────────────────────────────────────────────────────────────────────────────

def cosine_similarity(a: list[float], b: list[float]) -> float:
    va, vb = np.array(a), np.array(b)
    return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-9))


def find_top_nodes(
    question: str,
    db: Neo4jConnection,
    top_k: int = 3,
    labels: list[str] | None = None,
) -> list[dict]:
    """
    Embed the question and return the top_k most similar graph nodes.

    Args:
        question: Natural language question from the user.
        top_k:    Number of nodes to return.
        labels:   Restrict search to these labels (None = all labelled nodes).

    Returns:
        List of dicts with keys: label, name, score, properties.
    """
    q_vec = embed_batch([question])[0]

    if labels:
        filter_clause = " OR ".join(f"n:{lbl}" for lbl in labels)
        query = f"MATCH (n) WHERE ({filter_clause}) AND n.embedding IS NOT NULL RETURN n, labels(n)[0] AS lbl"
    else:
        query = "MATCH (n) WHERE n.embedding IS NOT NULL RETURN n, labels(n)[0] AS lbl"

    rows = db.read(query)

    scored = []
    for row in rows:
        props = row["n"]
        vec   = json.loads(props.get("embedding", "[]"))
        if not vec:
            continue
        score = cosine_similarity(q_vec, vec)
        scored.append({
            "label":      row["lbl"],
            "name":       props.get("name") or props.get("title", ""),
            "score":      score,
            "properties": props,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    with Neo4jConnection() as db:
        print("Computing embeddings for all graph nodes...")
        add_embeddings(db)
        print("\n✓ All embeddings stored.")

        # Quick test
        print("\nTest search: 'superhero team saving the world'")
        results = find_top_nodes("superhero team saving the world", db, top_k=3)
        for r in results:
            print(f"  [{r['label']:<15}] {r['name']:<40} score={r['score']:.3f}")

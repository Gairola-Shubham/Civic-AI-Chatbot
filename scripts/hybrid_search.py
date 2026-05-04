import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

# -----------------------------
# LOAD DATA
# -----------------------------
print("Loading data...")

with open("data_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]
metadata = chunks

# Load FAISS index
index = faiss.read_index("faiss_index.bin")

# Load embedding model
model = SentenceTransformer("intfloat/multilingual-e5-base")

# -----------------------------
# BM25 SETUP
# -----------------------------
tokenized_corpus = [text.split() for text in texts]
bm25 = BM25Okapi(tokenized_corpus)


# -----------------------------
# HELPER: CLEAN TEXT CHECK
# -----------------------------
def is_good_text(text):
    if not text or len(text.split()) < 25:
        return False

    weird_ratio = sum(1 for c in text if ord(c) > 3000) / len(text)
    if weird_ratio > 0.2:
        return False

    return True


# -----------------------------
# HYBRID SEARCH FUNCTION
# -----------------------------
def hybrid_search(query, top_k=5, alpha=0.6, filter_state=None, filter_domain=None):

    # -------- FAISS SEARCH --------
    query_embedding = model.encode(
        ["query: " + query],
        normalize_embeddings=True
    )

    D, I = index.search(query_embedding, top_k * 4)

    faiss_scores = D[0]
    faiss_indices = I[0]

    # Normalize FAISS scores
    if len(faiss_scores) > 0:
        faiss_scores = (faiss_scores - np.min(faiss_scores)) / (
            np.max(faiss_scores) - np.min(faiss_scores) + 1e-8
        )

    # -------- BM25 SEARCH --------
    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)

    bm25_top_indices = np.argsort(bm25_scores)[-top_k * 4:]
    bm25_top_scores = bm25_scores[bm25_top_indices]

    # Normalize BM25 scores
    if len(bm25_top_scores) > 0:
        bm25_top_scores = (bm25_top_scores - np.min(bm25_top_scores)) / (
            np.max(bm25_top_scores) - np.min(bm25_top_scores) + 1e-8
        )

    # -------- COMBINE SCORES --------
    score_dict = {}

    # FAISS scores
    for idx, score in zip(faiss_indices, faiss_scores):
        if idx < 0:
            continue
        score_dict[idx] = alpha * score

    # BM25 scores
    for idx, score in zip(bm25_top_indices, bm25_top_scores):
        if idx < 0:
            continue
        if idx in score_dict:
            score_dict[idx] += (1 - alpha) * score
        else:
            score_dict[idx] = (1 - alpha) * score

    # -------- SORT RESULTS --------
    sorted_results = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

    # -------- FILTER + DEDUP --------
    final_results = []
    seen_texts = set()

    for idx, score in sorted_results:
        r = metadata[idx]

        # ❌ Remove bad OCR chunks
        if not is_good_text(r["text"]):
            continue

        # ❌ Remove duplicates
        if r["text"] in seen_texts:
            continue

        # ❌ Filter by state
        if filter_state and r["state"].lower() != filter_state.lower():
            continue

        # ❌ Filter by domain
        if filter_domain and r["domain"].lower() != filter_domain.lower():
            continue

        seen_texts.add(r["text"])

        r_copy = r.copy()
        r_copy["score"] = float(score)

        final_results.append(r_copy)

        if len(final_results) >= top_k:
            break

    return final_results


# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":

    while True:
        query = input("\nEnter your query (or 'exit'): ")

        if query.lower() == "exit":
            break

        # Optional filters
        state = None
        domain = None

        results = hybrid_search(
            query,
            top_k=5,
            filter_state=state,
            filter_domain=domain
        )

        for i, r in enumerate(results):
            print(f"\nResult {i+1}")
            print(f"State: {r['state']} | Domain: {r['domain']}")
            print(f"Score: {round(r['score'], 3)}")
            print(r["text"][:400])
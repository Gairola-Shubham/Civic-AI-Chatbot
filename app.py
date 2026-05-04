from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import json
import faiss
import numpy as np
import re
import ollama

from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

# -----------------------------
# INIT FASTAPI
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# LOAD DATA
# -----------------------------
print("Loading data...")

with open("data_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]
metadata = chunks

index = faiss.read_index("faiss_index.bin")

model = SentenceTransformer("intfloat/multilingual-e5-base")

tokenized_corpus = [text.split() for text in texts]
bm25 = BM25Okapi(tokenized_corpus)

print("Data loaded successfully!")

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F\u0900-\u097F]+", "", text)
    return text.strip()

# -----------------------------
# DETECT STATE (🔥 NEW)
# -----------------------------
def detect_state(query):
    q = query.lower()
    if "delhi" in q:
        return "Delhi"
    elif "maharashtra" in q:
        return "Maharashtra"
    elif "uttar pradesh" in q or "up" in q:
        return "Uttar Pradesh"
    return None

# -----------------------------
# HYBRID SEARCH (UPDATED)
# -----------------------------
def hybrid_search(query, top_k=3, alpha=0.6, filter_state=None):

    query_embedding = model.encode(
        ["query: " + query],
        normalize_embeddings=True
    )

    D, I = index.search(query_embedding, top_k * 3)

    faiss_scores = D[0]
    faiss_indices = I[0]

    if len(faiss_scores) > 0:
        faiss_scores = (faiss_scores - np.min(faiss_scores)) / (
            np.max(faiss_scores) - np.min(faiss_scores) + 1e-8
        )

    tokenized_query = query.split()
    bm25_scores = bm25.get_scores(tokenized_query)

    bm25_top_indices = np.argsort(bm25_scores)[-top_k * 3:]
    bm25_top_scores = bm25_scores[bm25_top_indices]

    if len(bm25_top_scores) > 0:
        bm25_top_scores = (bm25_top_scores - np.min(bm25_top_scores)) / (
            np.max(bm25_top_scores) - np.min(bm25_top_scores) + 1e-8
        )

    score_dict = {}

    for idx, score in zip(faiss_indices, faiss_scores):
        if idx < 0:
            continue
        score_dict[idx] = alpha * score

    for idx, score in zip(bm25_top_indices, bm25_top_scores):
        if idx < 0:
            continue
        if idx in score_dict:
            score_dict[idx] += (1 - alpha) * score
        else:
            score_dict[idx] = (1 - alpha) * score

    sorted_results = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

    final_results = []

    for idx, score in sorted_results:
        r = metadata[idx]

        # 🔥 FILTER STATE
        if filter_state and r["state"].lower() != filter_state.lower():
            continue

        r_copy = r.copy()
        r_copy["score"] = float(score)
        final_results.append(r_copy)

        if len(final_results) >= top_k:
            break

    return final_results

# -----------------------------
# REQUEST MODEL
# -----------------------------
class QueryRequest(BaseModel):
    query: str

# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def home():
    return {"message": "Civic AI Chatbot is running"}

# -----------------------------
# CHAT
# -----------------------------
@app.post("/chat")
def chat(request: QueryRequest):

    query = request.query

    # 🔥 Detect state
    state = detect_state(query)

    # 🔍 Retrieve
    results = hybrid_search(query, top_k=3, filter_state=state)

    # ❌ LOW RELEVANCE CHECK (VERY IMPORTANT)
    if len(results) == 0 or results[0]["score"] < 0.25:
        return {
            "answer": "Not found in documents.",
            "sources": []
        }

    # 🧠 Context
    context = "\n\n".join([
        clean_text(r["text"])[:300]
        for r in results
    ])

    # 🔥 STRONG PROMPT (CRITICAL FIX)
    prompt = f"""
You are a Civic AI assistant.

STRICT RULES:
1. Answer ONLY from the given context.
2. Do NOT use outside knowledge.
3. If answer is not clearly present, say: "Not found in documents."
4. Do NOT guess or assume.
5. Do NOT mix unrelated topics or states.
6. Keep answer clear and concise.

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = ollama.chat(
            model="phi3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response["message"]["content"]

        # Clean output
        answer = re.sub(r"\s+", " ", answer)
        answer = answer.replace("*", "").replace("+", "")

    except Exception:
        answer = "⚠️ Model failed due to low memory or internal error."

    # 📌 Sources
    sources = [
        {
            "state": r["state"],
            "domain": r["domain"],
            "page": r["page"]
        }
        for r in results
    ]

    return {
        "answer": answer,
        "sources": sources
    }
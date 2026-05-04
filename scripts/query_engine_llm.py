import json
import faiss
import requests
from sentence_transformers import SentenceTransformer

INDEX_FILE = "faiss_index.bin"
METADATA_FILE = "metadata.json"
CHUNKS_FILE = "data_chunks.json"

TOP_K = 5

print("Loading embedding model...")
model = SentenceTransformer("intfloat/multilingual-e5-base")

print("Loading FAISS index...")
index = faiss.read_index(INDEX_FILE)

print("Loading chunks...")
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("System ready.\n")


def search_documents(query, top_k=5):

    query_embedding = model.encode(
        ["query: " + query],
        normalize_embeddings=True
    )

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, i in zip(scores[0], indices[0]):

        if score < 0.35:   # similarity threshold
            continue

        chunk = chunks[i]

        results.append({
            "text": chunk["text"],
            "source_file": chunk["source_file"],
            "source_path": chunk["source_path"],
            "score": float(score)
        })

    return results


def ask_llm(question, context):

    prompt = f"""
You are CivicAI, a chatbot that answers questions using Delhi Government documents.

RULES:
1. Use ONLY the provided context.
2. If the context does not contain the answer, respond exactly:
  "The information is not available in the dataset."
3. Do not guess or use outside knowledge.

Context:
{context}

Question:
{question}

Answer clearly and cite the document.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


while True:

    query = input("\nAsk question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    print("\nSearching documents...\n")

    results = search_documents(query)

    if len(results) == 0:
        print("\nThe information is not available in the dataset.")
        continue

    context = "\n\n".join([r["text"] for r in results])

    answer = ask_llm(query, context)

    print("\n================ ANSWER ================\n")
    print(answer)

    print("\n============= SOURCES =============\n")

    for r in results:
        print(f"Source File: {r['source_file']}")
        print(f"Path: {r['source_path']}")
        print("-" * 50)
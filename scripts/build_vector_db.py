import json
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "data_chunks.json"
INDEX_FILE = "faiss_index.bin"

print("Loading embedding model...")
model = SentenceTransformer("intfloat/multilingual-e5-base")

print("Loading chunks...")
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# -----------------------------
# PREPARE TEXTS
# -----------------------------
texts = []

for item in chunks:
    text = item["text"].strip()

    # Skip empty or bad text (extra safety)
    if not text or len(text.split()) < 10:
        continue

    # E5 format (IMPORTANT)
    texts.append("passage: " + text)

print(f"Total valid chunks: {len(texts)}")


# -----------------------------
# GENERATE EMBEDDINGS
# -----------------------------
print("Generating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=32,  # faster
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

dimension = embeddings.shape[1]


# -----------------------------
# BUILD FAISS INDEX
# -----------------------------
print("Building FAISS index...")

index = faiss.IndexFlatIP(dimension)  # cosine similarity
index.add(embeddings)

faiss.write_index(index, INDEX_FILE)

print(f"FAISS index saved to {INDEX_FILE}")
print("Vector DB created successfully!")
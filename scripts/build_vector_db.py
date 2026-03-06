import json
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "data_chunks.json"
INDEX_FILE = "faiss_index.bin"
METADATA_FILE = "metadata.json"

print("Loading embedding model...")
model = SentenceTransformer("intfloat/multilingual-e5-base")

print("Loading chunks...")
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = []
metadata = []

for item in chunks:
    texts.append("passage: " + item["text"])  # Important for E5 model
    metadata.append({
        "source_file": item["source_file"],
        "source_path": item["source_path"],
        "chunk_id": item["chunk_id"]
    })

print(f"Total chunks to embed: {len(texts)}")

print("Generating embeddings...")
embeddings = model.encode(
    texts,
    batch_size=16,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

dimension = embeddings.shape[1]

print("Building FAISS index...")
index = faiss.IndexFlatIP(dimension)  # cosine similarity
index.add(embeddings)

faiss.write_index(index, INDEX_FILE)

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False)

print("Vector database created successfully!")
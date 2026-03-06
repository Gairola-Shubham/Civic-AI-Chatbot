import os
import json
from pathlib import Path

DATA_DIR = "data_processed"
OUTPUT_FILE = "data_chunks.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


all_chunks = []

for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            text = clean_text(text)

            chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

            for idx, chunk in enumerate(chunks):
                all_chunks.append({
                    "text": chunk,
                    "source_file": file,
                    "source_path": file_path,
                    "chunk_id": idx
                })

print(f"Total chunks created: {len(all_chunks)}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print("Chunks saved to data_chunks.json")
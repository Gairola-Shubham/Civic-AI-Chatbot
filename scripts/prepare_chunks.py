import os
import json

DATA_DIR = "data_processed"
OUTPUT_FILE = "data_chunks.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# -----------------------------
# Chunking Function
# -----------------------------
def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if len(chunk.strip()) > 120:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# -----------------------------
# FINAL STRONG FILTER
# -----------------------------
def is_bad_chunk(text):
    words = text.split()

    # Too small
    if len(words) < 20:
        return True

    # Too many non-alphabetic words
    alpha_words = sum(1 for w in words if any(c.isalpha() for c in w))
    if alpha_words / len(words) < 0.6:
        return True

    # Too many numeric tokens (tables)
    numeric_words = sum(1 for w in words if w.isdigit())
    if numeric_words / len(words) > 0.3:
        return True

    # Too repetitive
    if len(set(words)) < len(words) * 0.5:
        return True

    return False


# -----------------------------
# Metadata Extraction (FIXED)
# -----------------------------
def extract_metadata(path):
    path = path.lower()

    # State detection
    if "delhi" in path:
        state = "Delhi"
    elif "maharashtra" in path:
        state = "Maharashtra"
    elif "uttar pradesh" in path:
        state = "Uttar Pradesh"
    else:
        state = "Unknown"

    # Domain detection
    if "budget" in path:
        domain = "Budget"
    elif "crime" in path:
        domain = "Crime"
    elif "environment" in path:
        domain = "Environment"
    elif "education" in path:
        domain = "Education"
    elif "health" in path:
        domain = "Health"
    elif "transport" in path:
        domain = "Transport"
    elif "gazette" in path:
        domain = "Gazette"
    elif "employment" in path or "economy" in path:
        domain = "Economy"
    else:
        domain = "General"

    return state, domain


# -----------------------------
# MAIN PROCESSING
# -----------------------------
all_chunks = []

for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            document_name = data.get("document_name", file)

            # 🔥 FIX: use original source path
            source_path = data.get("source_path", "")
            state, domain = extract_metadata(source_path)

            for page in data.get("pages", []):
                text = page.get("text", "")
                page_number = page.get("page_number", -1)
                language = page.get("language", "unknown")

                # 🔥 Language filter
                if language not in ["en", "hi", "mr"]:
                    continue

                if not text or len(text.strip()) < 100:
                    continue

                chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

                for idx, chunk in enumerate(chunks):

                    # 🔥 Remove headers
                    if any(x in chunk for x in [
                        "REGD", "GAZETTE", "No.", "PART",
                        "EXTRAORDINARY", "PUBLISHED",
                        "GOVERNMENT OF", "DEPARTMENT OF"
                    ]):
                        continue

                    # 🔥 Remove table-like chunks
                    if any(char.isdigit() for char in chunk[:50]) and chunk.count(" ") < 10:
                        continue

                    # 🔥 Garbage filter
                    if is_bad_chunk(chunk):
                        continue

                    all_chunks.append({
                        "text": chunk,
                        "document": document_name,
                        "page": page_number,
                        "language": language,
                        "state": state,
                        "domain": domain,
                        "chunk_id": f"{document_name}_{page_number}_{idx}"
                    })


print(f"Total chunks created: {len(all_chunks)}")


# -----------------------------
# SAVE OUTPUT
# -----------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print(f"Chunks saved to {OUTPUT_FILE}")
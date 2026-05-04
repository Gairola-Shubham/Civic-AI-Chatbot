import os
import re
import json
import unicodedata
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
from langdetect import detect

# -----------------------------
# CONFIG
# -----------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

RAW_DIR = "data_raw"
PROCESSED_DIR = "data_processed"
FAILED_LOG = "failed_files.txt"

os.makedirs(PROCESSED_DIR, exist_ok=True)


# -----------------------------
# Garbage Detection
# -----------------------------
def is_garbage(text):
    if not text or len(text.strip()) < 100:
        return True

    weird_chars = sum(1 for c in text if ord(c) > 3000)
    ratio = weird_chars / len(text)

    return ratio > 0.30


# -----------------------------
# Language Detection
# -----------------------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


# -----------------------------
# Clean Text
# -----------------------------
def clean_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Page \d+", "", text)
    text = re.sub(r"[^\w\s\u0900-\u097F.,]", "", text)
    return text.strip()


# -----------------------------
# Extract Using PyMuPDF
# -----------------------------
def extract_text_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text()

        pages.append({
            "page_number": i + 1,
            "text": text
        })

    return pages


# -----------------------------
# Extract Using OCR
# -----------------------------
def extract_text_ocr(path):
    print("Using OCR...")

    images = convert_from_path(path, dpi=200)
    pages = []

    for i, img in enumerate(images):
        text = pytesseract.image_to_string(
            img,
            lang="eng+hin+mar",
            config="--psm 6"
        )

        pages.append({
            "page_number": i + 1,
            "text": text
        })

    return pages


# -----------------------------
# Process Single PDF
# -----------------------------
def process_pdf(pdf_path):
    print(f"\nProcessing: {pdf_path}")

    pages = extract_text_pymupdf(pdf_path)

    # Check garbage using first few pages
    sample_text = " ".join([p["text"] for p in pages[:3]])

    if is_garbage(sample_text):
        pages = extract_text_ocr(pdf_path)
    else:
        print("Using normal extraction")

    processed_pages = []

    for page in pages:
        cleaned = clean_text(page["text"])

        # Skip very small pages
        if len(cleaned.split()) < 30:
            continue

        lang = detect_language(cleaned)

        processed_pages.append({
            "page_number": page["page_number"],
            "text": cleaned,
            "language": lang
        })

    if not processed_pages:
        print("Skipped empty/garbage document")
        return False

    output_data = {
        "document_name": Path(pdf_path).name,
        "source_path": pdf_path,
        "pages": processed_pages
    }

    # Preserve folder structure
    relative_path = os.path.relpath(pdf_path, RAW_DIR)

    output_file = os.path.join(
        PROCESSED_DIR,
        relative_path.replace(".pdf", ".json")
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Saved JSON: {output_file}")
    return True


# -----------------------------
# Load Failed Files
# -----------------------------
def load_failed_files():
    if not os.path.exists(FAILED_LOG):
        return []
    with open(FAILED_LOG, "r") as f:
        return [line.strip() for line in f.readlines()]


# -----------------------------
# Main Runner
# -----------------------------
if __name__ == "__main__":
    print("Starting script...")

    retry_mode = False  # Set True to retry failed files only

    # Optional: clear failed log for fresh run
    if not retry_mode and os.path.exists(FAILED_LOG):
        os.remove(FAILED_LOG)

    if retry_mode:
        pdf_files = load_failed_files()
        print(f"Retrying failed files: {len(pdf_files)}")
    else:
        pdf_files = []
        for root, dirs, files in os.walk(RAW_DIR):
            for file in files:
                if file.endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))

        print(f"Total PDFs found: {len(pdf_files)}")

    # -----------------------------
    # Processing Loop
    # -----------------------------
    for i, pdf in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing...")

        relative_path = os.path.relpath(pdf, RAW_DIR)

        output_file = os.path.join(
            PROCESSED_DIR,
            relative_path.replace(".pdf", ".json")
        )

        # Skip already processed
        if os.path.exists(output_file):
            print(f"Skipping (already done): {pdf}")
            continue

        try:
            success = process_pdf(pdf)

            if not success:
                with open(FAILED_LOG, "a") as log:
                    log.write(pdf + "\n")

        except Exception as e:
            print(f"Error processing {pdf}: {e}")

            with open(FAILED_LOG, "a") as log:
                log.write(pdf + "\n")

    print("\nDone!")
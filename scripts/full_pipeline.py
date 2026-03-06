import os
import fitz
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
from tqdm import tqdm

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

RAW_DIR = "data_raw"
PROCESSED_DIR = "data_processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)


def is_garbage(text):
    if not text or len(text.strip()) < 500:
        return True
    return False


def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


def extract_normal(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_ocr(pdf_path):
    images = convert_from_path(
        pdf_path,
        dpi=200,
        poppler_path=r"C:\poppler\poppler-25.12.0\Library\bin"  # 🔥 Explicit poppler path
    )

    full_text = ""
    for img in images:
        full_text += pytesseract.image_to_string(
            img,
            lang="hin+eng",
            config="--psm 6"
        )

    return full_text


def process_pdf(pdf_path):
    relative_path = os.path.relpath(pdf_path, RAW_DIR)
    output_path = os.path.join(PROCESSED_DIR, relative_path)
    output_path = output_path.replace(".pdf", ".txt")

    # Skip if already processed
    if os.path.exists(output_path):
        return

    print(f"\nProcessing: {pdf_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        text = extract_normal(pdf_path)

        if is_garbage(text):
            print("   → Using OCR...")
            text = extract_ocr(pdf_path)

        text = clean_text(text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        print("   ✓ Done")

    except Exception as e:
        print(f"   ✗ Error processing {pdf_path}")
        print(f"   {e}")


if __name__ == "__main__":
    pdf_files = []

    for root, dirs, files in os.walk(RAW_DIR):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    print(f"Total PDFs found: {len(pdf_files)}")

    for pdf in tqdm(pdf_files):
        process_pdf(pdf)
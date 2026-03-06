import os
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path

# Set Tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

RAW_DIR = "data_raw"
PROCESSED_DIR = "data_processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)


# -----------------------------
# Garbage Detection Function
# -----------------------------
def is_garbage(text):
    if not text or len(text.strip()) < 200:
        return True

    weird_chars = sum(1 for c in text if ord(c) > 3000)
    ratio = weird_chars / len(text)

    return ratio > 0.30


# -----------------------------
# Clean Text
# -----------------------------
def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


# -----------------------------
# Extract Using PyMuPDF
# -----------------------------
def extract_text_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    return full_text


# -----------------------------
# Extract Using OCR
# -----------------------------
def extract_text_ocr(path):
    print("Using OCR extraction...")

    images = convert_from_path(
        path,
        dpi=200,  # 🔥 faster than default 300
        poppler_path=r"C:\poppler\Library\bin"
    )

    full_text = ""

    for img in images:
        text = pytesseract.image_to_string(
            img,
            lang="hin+eng",
            config="--psm 6"
        )
        full_text += text

    return full_text


# -----------------------------
# Main Processing Function
# -----------------------------
def process_pdf(pdf_path):
    print(f"\nProcessing: {pdf_path}")

    # Try normal extraction first
    text = extract_text_pymupdf(pdf_path)

    # If garbage → OCR
    if is_garbage(text):
        print("Detected garbage or scanned PDF. Switching to OCR...")
        text = extract_text_ocr(pdf_path)
    else:
        print("Using normal text extraction.")

    text = clean_text(text)

    output_file = os.path.join(
        PROCESSED_DIR,
        Path(pdf_path).stem + ".txt"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved to: {output_file}")


# -----------------------------
# Run for All PDFs
# -----------------------------
if __name__ == "__main__":
    for file in os.listdir(RAW_DIR):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(RAW_DIR, file)
            process_pdf(pdf_path)
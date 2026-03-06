import os
import fitz
from tqdm import tqdm

RAW_DIR = "data_raw"

normal = []
needs_ocr = []

def is_garbage(text):
    if not text or len(text.strip()) < 500:
        return True
    return False

pdf_files = []

for root, dirs, files in os.walk(RAW_DIR):
    for file in files:
        if file.endswith(".pdf"):
            pdf_files.append(os.path.join(root, file))

print(f"Total PDFs: {len(pdf_files)}")

for pdf in tqdm(pdf_files):
    try:
        doc = fitz.open(pdf)
        text = ""
        for page in doc[:3]:  # Only first 3 pages for quick scan
            text += page.get_text()
        
        if is_garbage(text):
            needs_ocr.append(pdf)
        else:
            normal.append(pdf)

    except:
        needs_ocr.append(pdf)

print("\nNormal PDFs:", len(normal))
print("Needs OCR:", len(needs_ocr))
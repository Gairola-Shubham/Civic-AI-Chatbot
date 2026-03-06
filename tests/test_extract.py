import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pdf_path = "data_raw/1_dec_2015.pdf"


def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


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


print(f"\nTesting PDF: {pdf_path}")

text = extract_text_ocr(pdf_path)
text = clean_text(text)

print("\n--- Extracted Preview (First 1000 chars) ---\n")
print(text[:1000])
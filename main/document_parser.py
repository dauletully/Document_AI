import pdfplumber
from docx import Document
from pdf2image import convert_from_path
import easyocr
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
reader = easyocr.Reader(['en', 'ru'])

# def extract_text_from_pdf(path: str) -> str:
#     text = ""
#     with pdfplumber.open(path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() or ""
#     return text
def extract_text_from_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    
    # Если текста нет (скан), запускаем OCR
    if not text.strip():
        return extract_text_from_scan_pdf(path)
    return text


def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

# def extract_text_from_scan_pdf(path: str) -> str:
#     reader = easyocr.Reader(['en', 'ru'])
#     pages = convert_from_path(path, 300)

#     full_text = []
#     for i, page in enumerate(pages):
#         result = reader.readtext(page, detail=0)
#         page_text = "\n".join(result)
#         full_text.append(page_text)
#     return "\n\n".join(full_text)

def extract_text_from_scan_pdf(path: str) -> str:
    images = convert_from_path(path)
    full_text = []
    
    for img in images:
        img_np = np.array(img)
        result = reader.readtext(img_np, detail=0)
        full_text.append(" ".join(result))
    
    return "\n".join(full_text)

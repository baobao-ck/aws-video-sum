from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_file(filepath):
    if filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        return "\n".join(page.extract_text() for page in reader.pages)
    elif filepath.endswith(".docx"):
        doc = Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Unsupported file type")
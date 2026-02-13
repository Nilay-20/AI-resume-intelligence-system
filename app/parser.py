import pdfplumber # type: ignore
import os

def extract_text_from_pdf(pdf_path:str) -> str:
    text = "" 
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text +  "\n"
    return text.strip()


def extract_texts_from_folder(folder_path:str) -> str:
    resume_texts = {}

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            full_path = os.path.join(folder_path,filename)
            resume_texts[filename] = extract_text_from_pdf(full_path)
    return resume_texts


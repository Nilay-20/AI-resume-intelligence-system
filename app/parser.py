# import pdfplumber # type: ignore
# import os

# def extract_text_from_pdf(pdf_path:str) -> str:
#     text = "" 
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text(layout=True)
#             if page_text:
#                 text += page_text +  "\n"
#     return text.strip()


# def extract_texts_from_folder(folder_path:str) -> str:
#     resume_texts = {}

#     for filename in os.listdir(folder_path):
#         if filename.lower().endswith('.pdf'):
#             full_path = os.path.join(folder_path,filename)
#             resume_texts[filename] = extract_text_from_pdf(full_path)
#     return resume_texts

import fitz  # PyMuPDF #type: ignore
import os

def extract_texts_from_folder(folder_path):
    texts = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            doc = fitz.open(path)

            full_text = ""

            for page in doc:
                blocks = page.get_text("blocks")
                
                # Sort blocks by vertical position (y0), then horizontal (x0)
                blocks = sorted(blocks, key=lambda b: (b[1], b[0]))

                for block in blocks:
                    full_text += block[4] + "\n"

            texts[filename] = full_text

    return texts


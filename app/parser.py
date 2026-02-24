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

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract structured text from a single PDF using PyMuPDF (fitz).
    Preserves block order and line breaks for section parsing.
    """

    doc = fitz.open(file_path)
    full_text = ""

    for page in doc:
        # Extract text blocks with coordinates
        blocks = page.get_text("blocks")

        # Sort blocks top-to-bottom, then left-to-right
        blocks = sorted(blocks, key=lambda b: (b[1], b[0]))

        for block in blocks:
            block_text = block[4].strip()

            if block_text:
                full_text += block_text + "\n"

    doc.close()
    return full_text

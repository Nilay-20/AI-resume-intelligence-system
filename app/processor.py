# import re

# def clean_text(text: str) -> str:
#     # Normalize line endings
#     text = text.replace("\r\n", "\n")
#     text = text.replace("\r", "\n")

#     # Remove excessive blank lines but keep structure
#     text = re.sub(r"\n{2,}", "\n", text)

#     # Remove excessive spaces but DO NOT remove newlines
#     text = re.sub(r"[ \t]+", " ", text)

#     return text.strip()

import re

def clean_text(text: str) -> str:
    """
    Clean text while preserving line structure
    for section-based resume parsing.
    """

    # Normalize unicode quotes/dashes
    text = text.replace("’", "'").replace("–", "-")

    # Remove weird bullet symbols but keep line breaks
    text = re.sub(r"[•◦●▪■]", "", text)

    # Remove special characters but KEEP letters, numbers, newline
    text = re.sub(r"[^\w\s\n.,:/&+-]", "", text)

    # Normalize multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove extra blank lines
    text = re.sub(r"\n\s*\n", "\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text

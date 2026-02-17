import re
from app.sections import COMMON_SECTIONS

# ---- Precompile header regex ONCE ----
SECTION_HEADER_REGEX = {
    section: [
        re.compile(rf"^\s*{kw}\s*[:\-]?\s*$", re.IGNORECASE)
        for kw in keywords
    ]
    for section, keywords in COMMON_SECTIONS.items()
}


def extract_sections(text: str) -> dict:
    """
    Extract resume sections using line-aware parsing.
    Designed for PyMuPDF (fitz) extracted text.
    """

    sections = {section: "" for section in COMMON_SECTIONS}
    sections["other"] = ""

    current_section = "other"

    # IMPORTANT: rely on line structure from fitz
    lines = text.split("\n")

    for line in lines:
        line_stripped = line.strip()

        if not line_stripped:
            continue

        matched_section = None

        # Check if line is a section header
        for section, patterns in SECTION_HEADER_REGEX.items():
            for pattern in patterns:
                if pattern.match(line_stripped):
                    matched_section = section
                    break
            if matched_section:
                break

        if matched_section:
            current_section = matched_section
            continue

        # Append content
        sections[current_section] += line_stripped + " "

    # Final cleanup
    for section in sections:
        sections[section] = sections[section].strip()

    return sections

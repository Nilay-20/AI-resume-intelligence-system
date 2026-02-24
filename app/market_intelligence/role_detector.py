import re


HEADER_PATTERNS = [
    r"job title\s*[:\-]\s*(.+)",
    r"role\s*[:\-]\s*(.+)",
    r"position\s*[:\-]\s*(.+)",
    r"title\s*[:\-]\s*(.+)"
]


INTRO_PATTERNS = [
    r"hiring\s+(?:a|an)?\s*(.+)",
    r"looking for\s+(?:a|an)?\s*(.+)",
    r"seeking\s+(?:a|an)?\s*(.+)",
    r"position of\s+(?:a|an)?\s*(.+)"
]


ROLE_STOP_WORDS = [
    "who", "with", "to", "for",
    "responsible", "having",
    "required", "needed",
    "that", "and" , "location"
]


def clean_role(role_text: str) -> str:
    role_text = role_text.split("\n")[0]

    words = role_text.split()

    cleaned_words = []
    for word in words:
        if word.lower() in ROLE_STOP_WORDS:
            break
        cleaned_words.append(word)

    role = " ".join(cleaned_words)

    role = re.split(r"[,.|]", role)[0]

    return role.strip().title()


def detect_role(job_description: str) -> str:
    jd = job_description.lower()

    # ---------- HEADER EXTRACTION ----------
    for pattern in HEADER_PATTERNS:
        match = re.search(pattern, jd)
        if match:
            return clean_role(match.group(1))

    # ---------- INTRO SENTENCE ----------
    first_lines = "\n".join(jd.split("\n")[:5])

    for pattern in INTRO_PATTERNS:
        match = re.search(pattern, first_lines)
        if match:
            return clean_role(match.group(1))

    return "General Role"

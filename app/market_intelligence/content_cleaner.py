import re


MIN_SENTENCE_LENGTH = 40
MAX_TOTAL_CHARS = 50000


JUNK_PATTERNS = [
    r"cookie",
    r"privacy policy",
    r"terms of service",
    r"subscribe",
    r"sign up",
    r"login",
    r"all rights reserved",
    r"accept cookies",
    r"advertisement"
]


def remove_junk(text: str) -> str:
    """
    Remove common web junk patterns.
    """

    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        lower = line.lower()

        if any(junk in lower for junk in JUNK_PATTERNS):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def extract_valid_sentences(text: str):
    """
    Keep only informative sentences.
    """

    sentences = re.split(r"[.!?]", text)

    valid = [
        s.strip()
        for s in sentences
        if len(s.strip()) > MIN_SENTENCE_LENGTH
    ]

    return valid


def remove_duplicates(sentences):
    """
    Remove repeated sentences.
    """

    seen = set()
    unique = []

    for sentence in sentences:
        key = sentence.lower()

        if key not in seen:
            seen.add(key)
            unique.append(sentence)

    return unique


def normalize_text(sentences):
    """
    Normalize whitespace.
    """

    text = " ".join(sentences)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_market_content(raw_text: str) -> str:
    """
    Full cleaning pipeline.
    """

    text = remove_junk(raw_text)

    sentences = extract_valid_sentences(text)

    sentences = remove_duplicates(sentences)

    cleaned_text = normalize_text(sentences)

    return cleaned_text[:MAX_TOTAL_CHARS]


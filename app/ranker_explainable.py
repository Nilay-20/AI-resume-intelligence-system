import numpy as np #type: ignore
from sklearn.metrics.pairwise import cosine_similarity #type: ignore

def rank_resumes_explainable(
    resume_sections_map: dict,
    embedder,
    job_embedding: np.ndarray
):
    """
    Returns ranking with explainability:
    - final score
    - best matching section
    - per-section scores
    """

    results = []

    if len(job_embedding.shape) == 1:
        job_embedding = job_embedding.reshape(1, -1)

    for resume_name, sections in resume_sections_map.items():
        section_scores = {}
        max_score = 0.0
        best_section = None

        for section, text in sections.items():
            if not text.strip():
                continue

            section_embedding = embedder.embed_text(text)

            if len(section_embedding.shape) == 1:
                section_embedding = section_embedding.reshape(1, -1)

            score = cosine_similarity(section_embedding, job_embedding)[0][0]
            section_scores[section] = float(score)

            if score > max_score:
                max_score = score
                best_section = section

        results.append({
            "resume": resume_name,
            "score": max_score,
            "best_section": best_section,
            "section_scores": section_scores
        })

    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

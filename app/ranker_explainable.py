import numpy as np  # type: ignore
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

from app.market_intelligence.market_pipeline import get_market_context
from app.market_intelligence.market_scorer import compute_market_score
from app.market_intelligence.role_detector import detect_role


JD_WEIGHT = 0.7
MARKET_WEIGHT = 0.3


def rank_resumes_explainable(
    resume_sections_map: dict,
    embedder,
    job_embedding: np.ndarray,
    job_description: str
):
    """
    Returns ranking with explainability:
    - final score
    - JD score
    - Market score
    - best matching section
    - per-section scores
    """

    results = []

    # ---------- Ensure JD embedding shape ----------
    if len(job_embedding.shape) == 1:
        job_embedding = job_embedding.reshape(1, -1)

    # =====================================================
    # MARKET INTELLIGENCE (RUN ONLY ONCE)
    # =====================================================

    role = detect_role(job_description)

    market_context = get_market_context(role)

    market_embedding = embedder.embed_text(market_context)

    if len(market_embedding.shape) == 1:
        market_embedding = market_embedding.reshape(1, -1)

    # =====================================================
    # RESUME LOOP
    # =====================================================

    for resume_name, sections in resume_sections_map.items():

        section_scores = {}
        max_score = 0.0
        best_section = None

        combined_resume_text = ""

        # ---------- JD SECTION MATCHING ----------
        for section, text in sections.items():

            if not text.strip():
                continue

            combined_resume_text += " " + text

            section_embedding = embedder.embed_text(text)

            if len(section_embedding.shape) == 1:
                section_embedding = section_embedding.reshape(1, -1)

            score = cosine_similarity(
                section_embedding,
                job_embedding
            )[0][0]

            section_scores[section] = float(score)

            if score > max_score:
                max_score = score
                best_section = section

        jd_score = max_score

        # ---------- MARKET SCORE ----------
        resume_embedding = embedder.embed_text(combined_resume_text)

        if len(resume_embedding.shape) == 1:
            resume_embedding = resume_embedding.reshape(1, -1)

        market_score = compute_market_score(
            resume_embedding[0],
            market_embedding[0]
        )

        # ---------- FINAL WEIGHTED SCORE ----------
        final_score = (
            JD_WEIGHT * jd_score +
            MARKET_WEIGHT * market_score
        )

        results.append({
            "resume": resume_name,
            "final_score": float(final_score),
            "jd_score": float(jd_score),
            "market_score": float(market_score),
            "best_section": best_section,
            "section_scores": section_scores
        })

    # ---------- SORT BY FINAL SCORE ----------
    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return results
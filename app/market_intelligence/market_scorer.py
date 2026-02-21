from sklearn.metrics.pairwise import cosine_similarity


def compute_market_score(
    resume_embedding,
    market_embedding
):
    """
    Compute similarity between resume and
    market intelligence context.
    """

    score = cosine_similarity(
        [resume_embedding],
        [market_embedding]
    )[0][0]

    return float(score)
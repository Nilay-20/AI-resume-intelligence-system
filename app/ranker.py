from sklearn.metrics.pairwise import cosine_similarity #type: ignore
import numpy as np #type: ignore

def rank_resumes_by_sections(resume_sections_map: dict,embedder,job_embedding: np.ndarray) -> list:

    job_embedding = job_embedding.reshape(1, -1)
    results = []

    for resume_name, sections in resume_sections_map.items():
        section_texts = [text for text in sections.values() if text]

        if not section_texts:
            results.append((resume_name, 0.0))
            continue

        section_embeddings = embedder.embed_batch(section_texts)
        scores = cosine_similarity(section_embeddings, job_embedding)
        max_score = scores.max()

        results.append((resume_name, max_score))

    return sorted(results, key=lambda x: x[1], reverse=True)
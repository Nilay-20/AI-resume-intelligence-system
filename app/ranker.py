import numpy as np #type: ignore
from sklearn.metrics.pairwise import cosine_similarity #type: ignore

def rank_resumes(resume_embeddings: np.ndarray,resume_names: str,jd_embedding: np.ndarray) -> list:
    jd_embedding = jd_embedding.reshape(1,-1)

    scores = cosine_similarity(resume_embeddings,jd_embedding).flatten()

    results = list(zip(resume_names,scores))

    ranked_results = sorted(results,key = lambda x: x[1],reverse= True)

    return ranked_results
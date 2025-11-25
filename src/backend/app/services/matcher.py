from numpy import dot
from numpy.linalg import norm

def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

def match_cv_to_job(cv_embedding, job_embedding):
    score = float(cosine_similarity(cv_embedding, job_embedding))

    return {
        "similarity_score": score,
        "match_percentage": round(score * 100, 2)
    }

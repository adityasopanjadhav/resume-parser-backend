from app.services.job_embeddings import job_embeddings
from app.services.resume_embeddings import resume_embeddings


def match_jobs_for_resume(resume_id: str, top_k=5):

    chunks = resume_embeddings.get_resume_chunks(resume_id)

    if not chunks:
        return []
    

    # Use more chunks for better context (up to 10 chunks for ~5000 chars)
    query = " ".join(chunks[:min(10, len(chunks))])

    results = job_embeddings.job_store.similarity_search_with_relevance_scores(query, k=top_k)

    matched_jobs = [] 

    for doc, score in results:
        job_id = doc.metadata.get("job_id")
        matched_jobs.append({
            "job_id": doc.metadata.get("job_id"),
            "title": doc.metadata.get("title"),
            "company": doc.metadata.get("company"),
            "location": doc.metadata.get("location"),
            "score": round(score, 3)  # score is 0-1, already normalized (higher = better match)
        })

    return matched_jobs


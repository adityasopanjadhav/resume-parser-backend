from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os 

class JobEmbeddings:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        os.makedirs("./db/jobs", exist_ok=True)

        self.job_store = Chroma(
            collection_name="jobs",
            embedding_function=self.embeddings,
            persist_directory="./db/jobs"
        )

    
    def _build_job_document(self, job) -> Document:
        """ Convert document model to vector document """

        return Document(
            page_content=f""" 
            Title : {job.job_title}
            Company : {job.company_name}
            Description : {job.description}
            Required Skills : {','.join(job.required_skills or [])}
            Experience : {job.experience_years} years
            Location : {job.location}
            Salary Range : {job.salary_range}
            Job Type : {job.job_type}
            Job Status : {job.status.value}
            """,
            metadata={
                "job_id": str(job.job_id),
                "title": job.job_title,
                "company": job.company_name,
                "required_skills": ",".join(job.required_skills or []),
                "experience_years": str(job.experience_years),
                "location": job.location,
                "salary_range": job.salary_range,
                "job_type": job.job_type,
                "status": job.status.value
            }
        )
    

    def sync_add_job(self, job):
        """ Add a job to a ChromaDB after creating into the main database."""

        doc = self._build_job_document(job)
        self.job_store.add_documents([doc], ids=[str(job.job_id)])
        self.job_store.persist()
    
    def sync_update_job(self, job):

        try:
            self.job_store.delete(ids=[str(job.job_id)])
        except Exception as e:
            print(f"Error deleting job from vector store: {e}")
        
        doc = self._build_job_document(job)
        self.job_store.add_documents([doc], ids=[str(job.job_id)])
        self.job_store.persist()

    def sync_delete_job(self, job_id):
        try:
            self.job_store.delete(ids=[str(job_id)])
            self.job_store.persist()
        except Exception as e:
            print(f"Error deleting job from vector store: {e}")
        
    
    def rebuilt_vector_store(self,jobs):
        """ Rebuild the entire vector store from the main database."""
        self.job_store.delete_collection()

        for job in jobs:
            doc = self._build_job_document(job)
            self.job_store.add_documents([doc], ids=[str(job.job_id)])
            self.job_store.persist()
        
    def search_jobs(self, query, top_k=5):
        """ Search for similar jobs based on a query string. Returns top_k results."""
        results = self.job_store.similarity_search(query, k=top_k)
        return results
    

job_embeddings = JobEmbeddings()
    

        

        

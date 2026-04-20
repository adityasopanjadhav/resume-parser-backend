from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma 
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
import os 


class ResumeEmbeddings:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        os.makedirs("./db/resumes", exist_ok=True)


        self.resume_store = Chroma(
            collection_name="resumes",
            embedding_function=self.embeddings,
            persist_directory="./db/resumes"
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    
    def add_resume(self, text : str, user_id: str):

        resume_id = str(uuid.uuid4())

        chunks = self.text_splitter.split_text(text=text)

        documents = [] 
        ids = [] 

        for i , chunk in enumerate(chunks):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "resume_id": resume_id,
                        "chunk_id":i,
                        "user_id": user_id
                    }
                )
            )
            ids.append(f"{resume_id}_{i}")
        
        self.resume_store.add_documents(documents, ids=ids)
        self.resume_store.persist()

        return resume_id

    def get_resume_chunks(self, resume_id: str):
        results = self.resume_store._collection.get(where={"resume_id": resume_id})
        return results.get("documents", [])
    

    def delete_resume(self, resume_id):
        self.resume_store._collection.delete(
            where = {"resume_id": resume_id}
        )

        self.resume_store.persist()


    def search_resumes(self, query : str, user_id : str, top_k : int = 5):
        results = self.resume_store.similarity_search(
            query,
            k=top_k, 
            filter={"user_id": user_id})
        return results


resume_embeddings = ResumeEmbeddings()
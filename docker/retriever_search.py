from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.documents import Document

class RetrieverSearch:
    def __init__(self, 
                collection_name: str = "test_docker", 
                model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                url:str="http://localhost:6333"):
        self.collection_name = collection_name
        self.url = url
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.client = QdrantClient(url=self.url)
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name, 
            embedding=self.embeddings)
        
    def get_retriever(self, k: int = 4) -> QdrantVectorStore.as_retriever:
        """configure la recherche """
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k},
            
        )
    
    def search(self, query: str, k: int = 3) -> list[Document]:
        """Recherche simple où la query transformée en embedding"""
        retriever = self.get_retriever(k)
        results = retriever.invoke(query)
        return results
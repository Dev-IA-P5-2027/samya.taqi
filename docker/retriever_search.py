#uv pip install transformers sentencepiece accelerate langchain_mistralai python-dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient





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
        

        # self.generator = pipeline(
        #     "any-to-any",
        #     model="google/flan-t5-base"
        # )

        
       
    def search(self,query, k: int = 5, filter: dict = None):
        """configure la recherche  """
        return self.vector_store.similarity_search( 
            query,
            k=k,
            filter=filter

            )
    
    # def search(self, query: str, k: int = 3) -> list[Document]:
    #     """Recherche simple où la query transformée en embedding"""
    #     retriever = self.get_retriever(k)
    #     results = retriever.invoke(query)
    #     return results


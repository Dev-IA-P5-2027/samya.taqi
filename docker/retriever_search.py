#uv pip install transformers sentencepiece accelerate langchain_mistralai python-dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config import settings


class RetrieverSearch:
    def __init__(self ): #!url de qdrant dans le docker compose qdrant_container
        self.collection_name = settings.collection_name
        self.qdrant_url = settings.qdrant_url

        self.embeddings = HuggingFaceEmbeddings(model_name=settings.model_name)
        self.client = QdrantClient(url=self.qdrant_url)

        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name, 
            embedding=self.embeddings)
        
       
    def search(self,query, k: int = None, filter: dict = None):
        """configure la recherche  """
        k = k or settings.top_k
        return self.vector_store.similarity_search( 
            query,
            k=int(k),
            filter=filter
)
    

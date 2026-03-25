from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from uuid import uuid4
from langchain_core.documents import Document

client = QdrantClient(url="http://localhost:6333")
collection_name="demo_collection"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings,
)
retriever= vector_store.as_retriever(type_serach="similarity", search_kwargs={"k": 3})
reponse=retriever.invoke("What is the weather forecast for tomorrow?")
print(reponse)
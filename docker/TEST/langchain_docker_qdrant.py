
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from uuid import uuid4
from langchain_core.documents import Document
model_name="sentence-transformers/all-MiniLM-L6-v2"

# 1. Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name=model_name
)

# 2. Client Qdrant
client = QdrantClient(url="http://localhost:6333")

# 3. Test embedding

# 4. Création collection (taille corrigée)
collection_name = "test_docker"

# client.create_collection(
#     collection_name=collection_name,
#     vectors_config=VectorParams(size=client.get_embedding_size(model_name=model_name), distance=Distance.COSINE),
# )

# 5. Vector store
vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings,
)

# 6. Documents
documents = [
    Document(page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.", metadata={"source": "tweet"}),
    Document(page_content="The weather forecast for tomorrow is cloudy and overcast.", metadata={"source": "news"}),
    Document(page_content="Building an exciting new project with LangChain.", metadata={"source": "tweet"}),
    Document(page_content="Robbers broke into the city bank and stole $1 million.", metadata={"source": "news"}),
    Document(page_content="Wow! That was an amazing movie.", metadata={"source": "tweet"}),
    Document(page_content="Is the new iPhone worth the price?", metadata={"source": "website"}),
    Document(page_content="The top 10 soccer players in the world.", metadata={"source": "website"}),
    Document(page_content="LangGraph is great for agentic apps!", metadata={"source": "tweet"}),
    Document(page_content="The stock market is down 500 points.", metadata={"source": "news"}),
    Document(page_content="I have a bad feeling I am going to get deleted :(", metadata={"source": "tweet"}),
]

# 7. IDs
uuids = [str(uuid4()) for _ in range(len(documents))]

# 8. Ajout dans Qdrant
vector_store.add_documents(documents=documents, ids=uuids)

print(" Documents ajoutés avec succès !")
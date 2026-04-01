#pip install qdrant-client
#pip install fastembed

from qdrant_client import QdrantClient, models

# On remplace l'import OpenAI par HuggingFaceEmbeddings

client = QdrantClient(url="http://localhost:6333")

model_name = "sentence-transformers/all-MiniLM-L6-v2"
payload = [
    {"document": "Qdrant has Langchain integrations", "source": "Langchain-docs", },
    {"document": "Qdrant also has Llama Index integrations", "source": "LlamaIndex-docs"},
]
docs = [models.Document(text=data["document"], model=model_name) for data in payload]
ids = [42, 2]

client.create_collection(
    "test_docker",
    vectors_config=models.VectorParams(
        size=client.get_embedding_size(model_name), distance=models.Distance.COSINE)
)

client.upload_collection(
    collection_name="test_docker",
    vectors=docs,
    ids=ids,
    payload=payload,
)

search_result = client.query_points(
    collection_name="test_docker",
    query=models.Document(text="This is a query document", model=model_name)
).points
print(search_result)

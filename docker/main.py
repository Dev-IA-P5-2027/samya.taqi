

# def main():
#     data_path="./data"

#     pipeline=PipelineIngestion(data_path)
#     retriever=RetrieverSearch()
# #objectif 1: lire tous les pdfs , extraire le texte et créer une liste de documents
#     documents=pipeline.load_pdfs()
#     print(f'le nombre de pages chargés : {len(documents)}')
#     for doc in documents[:3]:
#         print("test document:", doc.page_content[:100])

# #objectif 2: diviser les documents en chunks
#     chunks= pipeline.split_documents(documents)
#     print(f'le nombre de chunks après split :{len(chunks)}')

# # #objectif 3: transformer les chunks en embeddings vectoriels
# #     split_documents=pipeline.transform_embeddings(split_documents)
# #     print(f'le nombre de chunks après la transformation en embeddings : {len(split_documents)}')  

# #objectif 3: transformer split en embeddings, et stocker les embeddings dans Qdrant
#     points = pipeline.qdrant_embeddings(chunks)
#     print(f"le nombre de chunks après la transformation en embeddings et le stockage dans Qdrant : {len(points)}")

# #objectif 4: rechercher les documents les plus similaires à une requete gérer par la classe RetrieverSearch
#     # results= retriever.search(k=3)
#     # for r, result in enumerate(results):
#     #     print(f"les réponses les plus pertinentes sont :{r+1}")
#     #     print(result.page_content) 
#     #     print(result.metadata["source"])

#     response=retriever.question_answer("comment aider un enfant?", k=3)
#     print(f"Réponse : {response}")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from config import Settings
from chain_rag import Chain

logging.basicConfig(level=logging.INFO)

app = FastAPI()

rag = Chain()

class RagApi(BaseModel):
    query: str
    k: int = 3
    search_type: str = "similarity"


@app.post("/ask")
def ask_question(query_request: RagApi):
    try:
        logging.info(f"Question reçue: {query_request.query}")

        result = rag.retriever_rag(
            query_request.query,
            k=query_request.k
        )

        return {
            "query": query_request.query,
            "response": str(result)
        }

    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "Welcome to the RAG API."}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from chain_rag import Chain
from config import settings
import uvicorn


# Configuration du logging
logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title="RAG API Assistant", 
    description="API pour un chatbot basé sur RAG utilisant Qdrant et MistralAI", 
    version="1.0",
    debug=settings.debug if hasattr(settings, "debug") else False
)


rag = Chain()

class RagApi(BaseModel):
    query: str
    k: int = settings.top_k
    search_type: str = "similarity" # "similarity" ou "hyde"

@app.post(
    "/ask", 
    tags=["Chatbot RAG"], 
    summary="Pose une question au chatbot RAG",
    description="Envoie une question au chatbot RAG et reçoit une réponse basée sur les documents similaires trouvés dans Qdrant."
)
async def ask(request: RagApi):
    try:
        logging.info(f"Question reçue: {request.query} (Type: {request.search_type})")
        
        # Appel de la chaîne avec les paramètres dynamiques
        response = rag.retriever_rag(
            query=request.query,
            search_type=request.search_type,
            k=request.k
        )
        return {"response": response}
    
    except Exception as e:
        logging.error(f"Erreur lors de la requête: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur interne: {str(e)}"
        )

@app.get("/", tags=["Système"])
async def root():
    return {"message": "Welcome to the RAG API Assistant!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
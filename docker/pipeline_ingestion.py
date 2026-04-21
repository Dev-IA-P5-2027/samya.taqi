#pip install qdrant-client langchain langchain-huggingface langchain-community transformers sentence-transformers  langchain_experimental  cryptography pypdf langchain-mistalai python-dotenv

import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient 
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from langchain_experimental.text_splitter import SemanticChunker
from uuid import uuid4
import logging
from config import settings

logging.basicConfig(level=logging.INFO)


class PipelineIngestion:
    """Pipeline d'ingestion de données pour la création d'une base vectorielle à partir des fichiers PDF"""
    def __init__(self):
        self.data_path = settings.data_path
        self.collection_name = settings.collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.model_name)

    """objectif 1: lire tous les pdfs , extraire le texte et créer une liste de documents"""
    def load_pdfs(self, limit:int| None=None) -> list[Document]:
        """lire tous les pdfs , extraire le texte et créer une liste de documents"""
        documents =[]

        for file in os.listdir(self.data_path): 
            if file.endswith(".pdf"):
                path=os.path.join(self.data_path, file) 
                loader = PyMuPDFLoader(path)
                try:
                    docs=loader.load() 
                except Exception as e:
                    logging.error(f"Erreur avce {file}:{e}")
                    continue

                for doc in docs:
                    doc.metadata["source"]=file

                documents.extend(docs) #Créer une liste de documents à partir de tous les fichiers pdfs de dossier data
        return documents[:limit] if limit else documents
    
    """objectif 2: split des documents et extraire du texte """
    def split_documents(self, documents: list[Document]) -> list[Document]:
        """découpage semantique des documents"""
        splitter=SemanticChunker(
            self.embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95
            )
        chunks=splitter.split_documents(documents)
        return chunks 


    """"Objectif 3: transformer les morceaux du texte en vecteur de nombre et les strocker dans une base vectorielle qdrant"""
    def store_in_qdrant(self, split_documents :list[Document], 
                    qdrant_url="host:'qdrant', port:6333"):
        """transformer les chunks en embeddings, et stocker les embeddings dans Qdrant"""
        
        client=QdrantClient(url=qdrant_url)
        #vérifier si la collection existe déjà sinon la créer
        
        try:
            client.get_collection(collection_name=self.collection_name)
        except Exception:
            vector_size=len(self.embeddings.embed_query("test"))
            client.create_collection(
                collection_name=self.collection_name,
                vectors_config= models.VectorParams(size=vector_size,
                                                    distance=Distance.COSINE)
            )
        
        #Génération des points à partir des chunks de documents et de leurs embeddings
        points=[]
        batch_size=64

        for i in range(0, len(self.split_documents), batch_size):
            batch_documents = self.split_documents[i:i+batch_size]
            batch_texts=[doc.page_content for doc in batch_documents]

            vectors = self.embeddings.embed_documents(batch_texts)
    
        for doc, vector in zip(split_documents,vectors):
            points.append(models.PointStruct(
                id=str(uuid4()), # 
                vector=vector,
                payload={"text": doc.page_content,
                        "source": doc.metadata.get("source"),
                        "page": doc.metadata.get("page")}
            ))

        client.upsert(
            collection_name=self.collection_name,
            points=points
        ) #envoie les données dans la base vectorielle Qdrant
        logging.info(f"{len(points):points ajoutés dans Qdrant}") #enregistrement des messages et des erreurs dans le programme lors de l'exécusion
        return points

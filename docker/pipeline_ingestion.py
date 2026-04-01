#pip install qdrant-client langchain langchain-huggingface langchain-community transformers sentence-transformers  langchain_experimental

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient 
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from langchain_experimental.text_splitter import SemanticChunker
from uuid import uuid4

class PipelineIngestion:
    """Pipeline d'ingestion de données pour la création d'une base vectorielle à partir des fichiers PDF"""
    def __init__(self, data_path: str,collection_name: str = "test_docker",model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        print(f"Dossier de données : {data_path}")
        self.data_path = data_path
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)

#objectif 1: lire tous les pdfs , extraire le texte et créer une liste de documents
    def load_pdfs(self ) -> list[Document]:
        """lire tous les pdfs , extraire le texte et créer une liste de documents"""
        documents =[]
        for file in os.listdir(self.data_path): 
            if file.endswith(".pdf"):
                path=os.path.join(self.data_path, file) 
                loader = PyPDFLoader(path) 
                docs=loader.load() 
                for doc in docs:
                    doc.metadata["source"]=file
                documents.extend(docs) #Créer une liste de documents à partir de tous les fichiers pdfs de dossier data
        return documents[:1]
    
#objectif 2: diviser les documents en morceaux 
    # def split_documents(self, documents: list[Document], chunk_size: int = 500, chunk_overlap: int = 50) -> list[Document]:
    #     """diviser les documents en chunks de taille 500 avec un chevauchement de 50"""
    #     splitter_text=RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    #     split_documents = splitter_text.split_documents(documents)
    #     return split_documents
    
    def split_documents(self, documents: list[Document]) -> list[Document]:
        """découpage semantique des documents"""
        splitter_semantic=SemanticChunker(self.embeddings)
        chunks=splitter_semantic.split_documents(documents)
        return chunks 


#objectif 3: transformer les chunks en embeddings vectoriels
    # def transform_embeddings(self, split_documents: list[Document]) -> list[Document]:
    #     embeddings=HuggingFaceEmbeddings (model_name="sentence-transformers/all-MiniLM-L6-v2")
    #     vector_embeddings=embeddings.embed_documents(
    #         [doc.page_content for doc in split_documents])
       
    #     for i, doc in enumerate(split_documents):
    #         doc.metadata["embedding"]=vector_embeddings[i]
    #     return split_documents

    def qdrant_embeddings(self, split_documents: list[Document], url="http://localhost:6333"):
        """transformer les chunks en embeddings, et stocker les embeddings dans Qdrant"""
        client=QdrantClient(url=url)
        #vérifier si la collection existe déjà, sinon la créer
        try:
            client.get_collection(collection_name=self.collection_name)
        except Exception:
            client.create_collection(
                collection_name=self.collection_name,
                vectors_config= models.VectorParams(size=384, distance=Distance.COSINE)
            )
        #Génération des points à partir des chunks de documents et de leurs embeddings
        points=[]
        texts =[doc.page_content for doc in split_documents]
        vectors=self.embeddings.embed_documents(texts) #transformer les chunks en embedding 
    
        for doc, vector in zip(split_documents,vectors):
            points.append(models.PointStruct(
                id=str(uuid4()),
                vector=vector,
                payload={"text": doc.page_content, "metadata": doc.metadata}
            ))
        client.upsert(
            collection_name=self.collection_name,
            points=points
        ) #envoie les données dans la base vectorielle Qdrant
        print()
        print(f'{len(points)} points sont ajoutés dans Qdrant')

        return points
    
    

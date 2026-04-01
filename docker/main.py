from pipeline_ingestion import PipelineIngestion
from retriever_search import RetrieverSearch

def main():
    data_path="./data"

    pipeline=PipelineIngestion(data_path)
    retriever=RetrieverSearch()
#objectif 1: lire tous les pdfs , extraire le texte et créer une liste de documents
    documents=pipeline.load_pdfs()
    print(f'le nombre de pages chargés : {len(documents)}')

#objectif 2: diviser les documents en chunks
    chunks= pipeline.split_documents(documents)
    print(f'le nombre de chunks après split :{len(chunks)}')

# #objectif 3: transformer les chunks en embeddings vectoriels
#     split_documents=pipeline.transform_embeddings(split_documents)
#     print(f'le nombre de chunks après la transformation en embeddings : {len(split_documents)}')  

#objectif 3: transformer split en embeddings, et stocker les embeddings dans Qdrant
    points = pipeline.qdrant_embeddings(chunks)
    print(f"le nombre de chunks après la transformation en embeddings et le stockage dans Qdrant : {len(points)}")

#objectif 4: rechercher les documents les plus similaires à une requete gérer par la classe RetrieverSearch
    results= retriever.search("comment aider les enfants à apprendre le français?", k=3)
    for r, doc in enumerate(results):
        print(f"les réponses les plus pertinentes sont :{r+1}  ")
        print(f"\n le contenu du document : {doc.page_content}")
        print(f"\n la source du document : {doc.metadata['source']}")



if __name__ == "__main__":
    main()
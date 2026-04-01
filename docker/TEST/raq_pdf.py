#pip install langchain pypdf chromadb pytest

# from langchain.document_loaders.pdf import PyPDFDirectoryLoarder
# def load_documents():
#     document_loader=PyPDFDirectoryLoarder(DATA_PATH)
#     return document_loader.load()
# documents =load_documents()
# print(documents[0]) #pour regarder comment documment sembler

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.schema.document import Document

# def split_documents(documents: list[Document]):
#     text_splitter=RecursiceCharacterTextSplitter(
#     chunk_size=800, 
#     chunk_overlap=80,
#     length_Function=len,
#     is_separator_regex=False,
#     )
#     return text_splitter.split_documents(documents)


# documents=load_documents()
# chunks=split_documents(documents)
# print(chunks[0])
#pip install langchain_text_splitters
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from get_embedding_function import get_embedding_function
from langchain_core.documents import Document
import uuid

#_____charger les pdf_______
def load_documents():
    docs = []

    pdf1 = PyPDFLoader(r"data\monopoly.pdf")
    pdf2 = PyPDFLoader(r"data\ticket_to_ride.pdf")

    docs.extend(pdf1.load())
    docs.extend(pdf2.load())
    return docs

#_____chunking_____
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    return splitter.split_documents(documents)

documents = load_documents()
chunks = split_documents(documents)

print("Nombre de chunks :", len(chunks))
print(chunks[1])
print(f"Nombre de documents chargés : {len(documents)}")

CHROMA_PATH="./chroma_db"
def add_to_chroma(chunks: list[Document]):
    db=Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=get_embedding_function()
    )
    #création ids uniques
    ids = [str(uuid.uuid4()) for _ in chunks]
    db.add_documents(chunks, ids=ids)
    db.persist() #sauvegarder la base de donnée
    print("Documents ajoutés à chroma")
add_to_chroma(chunks)
 #_____update data base____

def update_chroma(chunks):
    db=Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )
    existing_items=db.get(include=[]) #IDS sont tjrs incllus par defaut
    existing_ids=set(existing_items["ids"])
    print(f"le nombre de documents existent en base de données:{len(existing_ids)}")


#___ajouter les documments qui n'existe pas en base de données______
    new_chunks=[]
    new_ids=[]
    for chunk in chunks:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
            new_ids.append(chunk.metadata["id"])
     #ajouter seulement nouveaux
    if new_chunks:
        db.add_documents(new_chunks, ids=new_ids)
        db.persist()
        print(f" {len(new_chunks)} nouveaux chunks ajoutés")
    else:
        print("Aucun nouveau document à ajouter")
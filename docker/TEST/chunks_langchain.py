from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import document

text_splitter=RecursiveCharacterTextSplitter(
chunk_size=1000,  #la taille max de découpage de caractéres à retourner
chunk_overlap=200, #chevauchement entre chunks 
add_start_insdex=True, #index dans le document original
)
all_splits= text_splitter.split_documents(docs)

print(f"Split blog post into {len(all_splits)}sub_documents.")
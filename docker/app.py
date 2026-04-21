# import streamlit as st
# import requests

# query = st.text_input("Pose ta question")

# if st.button("Envoyer"):
#     res = requests.post("http://fastapi_backend:8000/ask", json={"query": query})  #!url de l'API FastAPI fastapi_backend dans le docker compose
#     response_text = res.json()["response"]
#     st.write(response_text)


import streamlit as st
import requests

st.set_page_config(page_title="Assistant RAG", page_icon="🤖")

st.title(" Chatbot basé sur RAG")

API_URL = "http://fastapi_backend:8000"


#sidebar pour les paramètres de recherche et chargements de documents
st.sidebar.header("⚙️ Paramètres")

# Sélection du nombre de documents à récupérer depuis la base vectorielle Qdrant
k = st.sidebar.selectbox("Nombre de documents à récupérer (k)", options=range(1, 11), index=2)

# Chargements de documents
uploaded_files = st.sidebar.file_uploader(
    "Charger des documents",
    type=["pdf", "markdown", "txt"],
    accept_multiple_files=True
)

# Bouton pour envoyer les fichiers
if st.sidebar.button(" Indexer les documents"): #on prépare les fichiers pour l'indexation en les envoyant à l'API FastAPI
    if uploaded_files:
        with st.sidebar.spinner("Indexation en cours..."):
            try:
                files = [
                    ("files", (file.name, file, file.type))
                    for file in uploaded_files
                ]
                res = requests.post(f"{API_URL}/upload", files=files)
                st.sidebar.success("Documents indexés !")
            except Exception as e:
                st.sidebar.error(f"Erreur upload : {e}")
    else:
        st.sidebar.warning(" Aucun fichier sélectionné !!")

#Section principale pour la conversation avec le chatbot RAG
if "messages" not in st.session_state:
    st.session_state.messages = [] #historique de la conversation

# Affichage historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# input utilsateur pose une question
if prompt := st.chat_input("Pose ta question ici..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(" Réflexion en cours..."):
            try:
                res = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "query": prompt,
                        "k": k   
                    }
                )

                res.raise_for_status()
                response_text = res.json()["response"]

                st.markdown(response_text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text
                })

            except Exception as e:
                st.error(f"Erreur : {e}")

# supprimer le historique de la conversation
if st.sidebar.button("Effacer la conversation"):
    st.session_state.messages = []
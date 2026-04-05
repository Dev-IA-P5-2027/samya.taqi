import streamlit as st
import requests

query = st.text_input("Pose ta question")

if st.button("Envoyer"):
    res = requests.post("http://localhost:8000/ask", json={"query": query})
    st.write(res.json()["response"])
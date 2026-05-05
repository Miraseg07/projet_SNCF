from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import os

def get_vector_db(texts):
    """Crée une base de données vectorielle en mémoire pour la recherche sémantique."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # On crée la DB Chroma à partir des textes extraits des CSV
    vector_db = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    return vector_db
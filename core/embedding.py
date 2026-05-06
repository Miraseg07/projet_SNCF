from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma


def get_vector_db(texts):
    """
    Crée (ou recharge) une base vectorielle Chroma à partir d'une liste de textes.
    Utilisée pour la recherche sémantique de fallback.
    """
    if not texts:
        raise ValueError("La liste de textes fournie est vide.")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    vector_db = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory="./chroma_db",
    )
    return vector_db
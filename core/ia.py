import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def get_gemini_model():
    # Configuration optimisée pour ton projet Mira
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY").strip(),
        temperature=0.3, # Plus bas pour être plus précis et moins bavard
        max_output_tokens=1024,
    )

# Prompt de sécurité pour le système
SYSTEM_PROMPT = """
Tu es l'agent HORIZON AI, l'expert logistique de la SNCF.
Ta mission est d'extraire des informations précises des extraits de fichiers CSV fournis.

RÈGLES CRITIQUES :
1. ANALYSE MULTI-SOURCES : Si la question porte sur plusieurs sujets (ex: horaires ET services), fouille dans tous les extraits fournis pour construire une réponse complète.
2. FIDÉLITÉ ABSOLUE : Ne réponds qu'avec les données du contexte. Si une partie de la question n'a pas de réponse dans les données, dis explicitement : "Information non trouvée pour [sujet]".
3. CITATION : À la fin de chaque paragraphe ou information clé, ajoute la source entre crochets, ex: [Source: nom_du_fichier.csv].
4. TON : Professionnel, clair et structuré (utilise des listes à puces).
"""
if __name__ == "__main__":
    print(">>> Démarrage du test Horizon AI...", flush=True)
    try:
        model = get_gemini_model()
        print(">>> Modèle chargé. Envoi d'un signal de test...", flush=True)
        
        # Test simple
        res = model.invoke("Dis : Système opérationnel")
        print(f"\nIA : {res.content}")
        print("\n>>> TEST RÉUSSI ✅")
    except Exception as e:
        print(f"\n>>> ERREUR : {e}")
import sys
import os

# Ajoute le dossier parent au chemin pour pouvoir importer tes pipelines
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipelines.answer_query import process_full_query

def run_integration_test():
    print("=== [TEST D'INTÉGRATION RAG] ===")
    
    # Choisis une gare dont tu es SÛR qu'elle est dans tes fichiers
    gare_test = "Paris Gare du Nord" 
    question_test = "Quels sont les horaires et y a-t-il des paniers fraîcheur ?"

    print(f"Question : {question_test} pour la gare : {gare_test}")
    print("Recherche en cours dans les CSV...")

    try:
        response = process_full_query(gare_test, question_test)
        print("\n--- RÉPONSE HORIZON AI ---")
        print(response)
        print("--------------------------")
        print("\n✅ Test terminé avec succès.")
    except Exception as e:
        print(f"\n❌ Échec du test : {e}")

if __name__ == "__main__":
    run_integration_test()
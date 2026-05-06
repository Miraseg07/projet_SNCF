import sys
import os
from datetime import datetime


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import de la fonction de réponse
try:
    from pipelines.answer_query import process_full_query
except ImportError:
    print("\n ERREUR : Impossible de trouver 'process_full_query'.")
    print("Vérifiez que votre fichier s'appelle 'answer_query.py' et se trouve dans le dossier 'pipelines'.")
    sys.exit(1)

def run_integration_test():
    # Dossier de log pour garder une trace écrite
    os.makedirs("TEST", exist_ok=True)
    log_file = "TEST/historique_reponses.txt"

    
    scenarios = [
        # Tests sur Paris Gare du Nord (Multi-thèmes)
        ("Paris Gare du Nord", "Bonjour ! Quels sont les horaires d'ouverture de la gare et proposez-vous des paniers fraîcheur ?"),
        ("Paris Gare du Nord", "Je m'ennuie un peu en attendant mon train, y a-t-il un piano ou des histoires à lire ?"),
        ("Paris Gare du Nord", "Est-ce qu'il y a des équipements pour aider une personne en fauteuil roulant ?"),
        
        # Tests Services & Détente
        ("Gare de Lyon", "Coucou Horizon AI ! J'ai 1h à tuer, qu'est-ce que je peux faire pour m'occuper un peu ?"),
        ("Aix-en-Provence TGV", "Bonjour, j'ai besoin de travailler mais je n'ai plus de batterie. Vous avez une solution ?"),
        
        # Tests Paniers & Horaires
        ("Rosa Parks", "Salut ! Je voudrais acheter des légumes frais ce soir, c'est possible ?"),
        ("Asnieres-sur-Seine", "Bonjour ! À quelle heure ferme la gare et où se trouvent les paniers fraîcheur ?"),
        
        # Test Accessibilité spécifique
        ("Marne-la-Vallee Chessy", "Bonjour, je voyage avec une personne handicapée, quelle aide est disponible en gare ?"),
        
        # Test Hors-Sujet
        ("Gare de Lyon", "Quel temps fait-il à Paris demain ?")
    ]

    print(f"\n{'='*70}")
    print(f" BATTERIE DE TESTS : HORIZON AI (Version Chaleureuse)")
    print(f"Nombre de cas à tester : {len(scenarios)}")
    print(f"{'='*70}\n")

    # Nettoyage du fichier log au début du test
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"SESSION DE TEST DU {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

    for i, (gare, question) in enumerate(scenarios, 1):
        print(f" [{i}/{len(scenarios)}] GARE : {gare}")
        print(f" QUESTION : {question}")
        
        try:
            # Appel du pipeline
            response = process_full_query(gare, question)

            # Affichage console
            print(f"\n✨ RÉPONSE D'HORIZON AI :")
            print(f"{response}")
            print(f"{'-'*70}\n")

            # Sauvegarde fichier
            log_entry = (
                f"TEST {i} | GARE: {gare}\n"
                f"QUESTION: {question}\n"
                f"REPONSE:\n{response}\n"
                f"{'-'*40}\n\n"
            )
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)

        except Exception as e:
            print(f" ERREUR pour {gare} : {e}\n")

    print(f"{'='*70}")
    print(f" TESTS TERMINÉS")
    print(f"Résultats détaillés disponibles dans : {log_file}")
    print(f"{'='*70}")

if __name__ == "__main__":
    run_integration_test()
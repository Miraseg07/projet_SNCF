import re
import time
import os
from core.ia import get_gemini_model
from pipelines.source_processing import SourceProcessor

def process_full_query(station_name, user_question, max_retries=5):
    """
    Orchestre la recherche de données locales et la génération de réponse par l'IA.
    """
    #  Configuration des chemins
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    data_path = os.path.join(base_dir, "data_source")
    
    print(f"\n--- DEBUT ANALYSE : {station_name} ---")
    
    # 2. Initialisation des composants
    model = get_gemini_model()
    processor = SourceProcessor(data_path)
    q_lower = user_question.lower()
    
    #  KEYWORDS MAP :On ajoute tous les synonymes pour que l'IA trouve toujours le bon fichier CSV
    
    themes_to_search = ["gare_info"] # Toujours inclure les infos de base
    
    keywords_map = {
        "horaire_gare": [
            "horaire", "ouvert", "ferme", "heure", "quand", "matin", "soir", "nuit", 
            "ouverture", "fermeture", "planning", "horaires", "fermee", "ouverte"
        ],
        "accessibilite": [
            "pmr", "fauteuil", "ascenseur", "aide", "handicap", "rampe", "handicape", 
            "accessibilite", "equipement", "roulant", "escalier", "escalator", 
            "deficient", "visuel", "accompagnement", "assistance"
        ],
        "services": [
            "faire", "occuper", "attendre", "temps", "piano", "histoire", "recharger", 
            "jouer", "ennuie", "wifi", "prise", "travailler", "distraction", "musique", 
            "lecture", "borne", "batterie", "work", "station", "loisir", "attente"
        ],
        "panier": [
            "panier", "legume", "fruit", "fraicheur", "frais", "manger", "achat", 
            "nourriture", "courses", "marche", "produit", "terroir", "agriculteur"
        ]
    }
    
    # Détection des thèmes présents dans la question
    for theme, keywords in keywords_map.items():
        if any(w in q_lower for w in keywords):
            themes_to_search.append(theme)
            print(f"DEBUG: Thème détecté -> {theme}")
    
    #  Extraction des données (RAG)
    context_chunks = []
    for theme in themes_to_search:
        data = processor.extract_targeted_data(station_name, theme)
        if data:
            context_chunks.extend(data)

    # Suppression des doublons et formatage du texte
    context_text = "\n".join(list(dict.fromkeys(context_chunks)))

    #  Sécurité : Si aucun contexte n'est trouvé
    if not context_text.strip():
        return f"Bonjour ! Je suis HORIZON AI. Je n'ai malheureusement pas trouvé d'informations spécifiques dans mes registres pour la gare de {station_name}."

    #  Prompting Expert
    final_prompt = f"""
Tu es HORIZON AI, l'assistant digital officiel de la SNCF. Ton ton est chaleureux, aidant et professionnel.

CONSIGNES STRICTES :
1. Salue toujours le voyageur avec élégance.
2. Réponds UNIQUEMENT en utilisant les informations du contexte ci-dessous.
3. Si une information manque (ex: horaire de fermeture), dis-le poliment au lieu d'inventer.
4. Pour les 'Paniers Fraîcheur' : précise toujours l'emplacement (ex: Parvis), le jour et le créneau horaire.
5. Ne cite jamais les noms des fichiers techniques (.csv).

CONTEXTE EXTRAIT DES REGISTRES :
{context_text}

QUESTION DU VOYAGEUR : {user_question}
"""

    # Appel IA avec gestion robuste des erreurs (Wait Time)
    wait_time = 3 
    for attempt in range(max_retries):
        try:
            response = model.invoke(final_prompt)
            return response.content
        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                print(f"DEBUG: Rate limit (429). Attente de {wait_time}s...")
                time.sleep(wait_time)
                wait_time *= 2 
                continue
            else:
                print(f" Erreur critique IA : {error_str}")
                return "Désolé, je rencontre une difficulté technique pour accéder aux informations. Réessayez dans un instant !"

    return "Le service est momentanément saturé suite à une forte affluence."
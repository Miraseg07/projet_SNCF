from core.ia import get_gemini_model, SYSTEM_PROMPT
from pipelines.source_processing import SourceProcessor

def process_full_query(station_name, user_question):
    model = get_gemini_model()
    
    # --- IMPORTANT : SI TES FICHIERS SONT DANS LE MÊME DOSSIER QUE LE SCRIPT, METS "." ---
    # SI ILS SONT DANS UN DOSSIER NOMMÉ data_source, GARDE "data_source/"
    processor = SourceProcessor("data_source/") 
    
    q_lower = user_question.lower()
    context_chunks = []

    print(f"🤖 DEBUG: Analyse de la question : '{user_question}'")

    # Aiguillage
    if "horaire" in q_lower and ("panier" in q_lower or "fraicheur" in q_lower):
        print("💡 DEBUG: Direction thématique -> HORAIRES PANIERS")
        context_chunks.extend(processor.extract_targeted_data(station_name, theme="panier"))
    
    elif "horaire" in q_lower:
        print("💡 DEBUG: Direction thématique -> HORAIRES GARE")
        context_chunks.extend(processor.extract_targeted_data(station_name, theme="horaire_gare"))

    if ("panier" in q_lower or "fraicheur" in q_lower) and not context_chunks:
        print("💡 DEBUG: Direction thématique -> PRÉSENCE PANIERS")
        context_chunks.extend(processor.extract_targeted_data(station_name, theme="panier"))

    # Synthèse du contexte
    context_text = "\n".join(list(set(context_chunks)))

    if not context_text:
        print("🚫 DEBUG: Le contexte final est VIDE. L'IA ne peut pas répondre.")
        return f"Désolé, je n'ai trouvé aucune donnée concernant votre demande pour la gare : {station_name}."

    print(f"📝 DEBUG: Envoi de {len(context_chunks)} extraits à Gemini...")

    final_prompt = f"""
    {SYSTEM_PROMPT}
    Tu es l'assistant HORIZON AI. Réponds à la question en utilisant le contexte fourni.
    CONTEXTE :
    {context_text}
    QUESTION : {user_question}
    """

    try:
        response = model.invoke(final_prompt)
        return response.content
    except Exception as e:
        return f"Erreur Gemini : {e}"
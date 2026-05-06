import pandas as pd
import os
import unicodedata
import re

class SourceProcessor:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.map_sources = {
            "horaire_gare": ["horaires-des-gares1.csv"],
            "panier": ["paniers-fraicheur.csv"],
            "gare_info": ["gares-de-voyageurs.csv"],
            "accessibilite": ["equipements-accessibilite-en-gares.csv", "referentiel-equipements-gares-.csv"],
            "services": ["service-d-attente-en-gare-api.csv"] 
        }

    def normalize(self, text):
        """Normalisation avancée pour gérer les tirets et les accents."""
        if not isinstance(text, str): text = str(text)
        text = text.lower()
        text = text.replace("-", " ") # Important pour gares type "Asnières-sur-Seine"
        text = unicodedata.normalize("NFD", text)
        text = "".join(c for c in text if unicodedata.category(c) != "Mn")
        text = re.sub(r"[^a-z0-9 ]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def extract_keywords(self, query_norm):
        STOPWORDS = {"gare", "de", "du", "la", "le", "les", "sur", "sous", "en", "et", "a", "au", "aux", "l", "d", "des"}
        words = set(query_norm.split()) - STOPWORDS
        return words

    def fuzzy_match(self, query_norm, cell_norm):
        """Matching robuste basé sur l'intersection des mots-clés."""
        if query_norm in cell_norm or cell_norm in query_norm: 
            return True
        query_words = self.extract_keywords(query_norm)
        cell_words = self.extract_keywords(cell_norm)
        if not query_words: return False
        
        # On valide si 80% des mots de la recherche sont présents dans la cellule
        intersection = query_words.intersection(cell_words)
        return len(intersection) / len(query_words) >= 0.8

    def extract_targeted_data(self, station_name, theme):
        results = []
        files_to_scan = self.map_sources.get(theme, [])
        query_norm = self.normalize(station_name)
        
        PRIORITY_COLUMNS_MAP = {
            "paniers-fraicheur.csv": ["Gare", "Nom_Gare"],
            "horaires-des-gares1.csv": ["Gare", "Nom_Gare"],
            "gares-de-voyageurs.csv": ["Nom_Gare", "Gare"],
             # On ajoute "Gare" ici au cas où
            "equipements-accessibilite-en-gares.csv": ["Nom de la gare", "Gare"], 
             # TRÈS IMPORTANT : On ajoute "Nom de la gare" car c'est ce qu'il y a dans ton fichier
            "referentiel-equipements-gares-.csv": ["Nom de la gare", "Gare", "Nom_Gare"], 
            "service-d-attente-en-gare-api.csv": ["Gare", "Nom_Gare"]
        }

        for filename in files_to_scan:
            path = os.path.join(self.data_folder, filename)
            if not os.path.exists(path): continue

            try:
                df = pd.read_csv(path, sep=';', engine="python", encoding="utf-8", on_bad_lines="skip")
                if len(df.columns) <= 1:
                    df = pd.read_csv(path, sep=None, engine="python", encoding="utf-8", on_bad_lines="skip")
            except:
                df = pd.read_csv(path, sep=None, engine="python", encoding="latin-1", on_bad_lines="skip")

            priority_cols = PRIORITY_COLUMNS_MAP.get(filename, [])
            valid_cols = [c for c in priority_cols if c in df.columns]
            
            if not valid_cols:
                mask = df.apply(lambda row: self.fuzzy_match(query_norm, self.normalize(" ".join(map(str, row.values)))), axis=1)
            else:
                mask = df.apply(lambda row: self.fuzzy_match(query_norm, self.normalize(" ".join([str(row[c]) for c in valid_cols]))), axis=1)
            
            matches = df[mask]

            if not matches.empty:
                # Ajout d'un log pour confirmer que la donnée est bien trouvée
                print(f"DEBUG SOURCE: [{theme}] Match trouvé dans {filename}")
                for _, row in matches.iterrows():
                    details = [f"{c}: {v}" for c, v in row.items() if pd.notna(v) and str(v).lower() != "nan" and "uic" not in c.lower()]
                    results.append(f"[Source: {theme}] " + " | ".join(details))
        
        return results

    # AJOUT POUR L'INTERFACE WEB 
    def get_all_stations(self):
        """Récupère la liste de toutes les gares pour la liste déroulante HTML."""
        path = os.path.join(self.data_folder, "gares-de-voyageurs.csv")
        if os.path.exists(path):
            try:
                df = pd.read_csv(path, sep=';', engine="python", on_bad_lines="skip")
                if 'Nom_Gare' in df.columns:
                    return sorted(df['Nom_Gare'].dropna().unique().tolist())
            except Exception as e:
                print(f"Erreur extraction liste gares: {e}")
        return []
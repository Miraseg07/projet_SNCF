import pandas as pd
import os

class SourceProcessor:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        # Vérifie bien que ces noms correspondent à tes fichiers sur ton bureau !
        self.map_sources = {
            "horaire_gare": ["horaires-des-gares1.csv"],
            "panier": ["paniers-fraicheur.csv"],
            "gare_info": ["gares-de-voyageurs.csv"],
            "accessibilite": ["equipements-accessibilite-en-gares.csv", "referentiel-equipements-gares-.csv"]
        }

    def extract_targeted_data(self, station_name, theme):
        results = []
        files_to_scan = self.map_sources.get(theme, [])
        
        # On nettoie pour ne garder que "Nord" si on cherche "Paris Gare du Nord"
        name_parts = [w for w in station_name.lower().split() if w not in ["gare", "du", "de", "la", "paris"]]
        if not name_parts: 
            name_parts = [station_name.lower()]

        print(f"\n🔍 DEBUG: Recherche du thème '{theme}' pour les mots-clés: {name_parts}")

        for filename in files_to_scan:
            path = os.path.join(self.data_folder, filename)
            
            # --- DEBUG : Vérification existence fichier ---
            if not os.path.exists(path):
                print(f"❌ DEBUG: Fichier INTROUVABLE : {path}")
                continue
            
            print(f"📂 DEBUG: Lecture de {filename}...")

            try:
                # Lecture flexible
                df = pd.read_csv(path, sep=None, engine='python', encoding='latin-1')
                
                # Filtrage
                mask = df.apply(lambda row: any(k in str(row.values).lower() for k in name_parts), axis=1)
                matches = df[mask]
                
                if not matches.empty:
                    print(f"✅ DEBUG: {len(matches)} ligne(s) trouvée(s) dans {filename}")
                    for _, row in matches.iterrows():
                        details = [f"{c}: {v}" for c, v in row.items() if pd.notna(v) and str(v).lower() != 'nan']
                        results.append(f"[Source: {filename}] " + " | ".join(details))
                else:
                    print(f"⚠️ DEBUG: Aucune ligne ne contient {name_parts} dans {filename}")

            except Exception as e:
                print(f"🔥 DEBUG: Erreur lors de la lecture de {filename}: {e}")
        
        return results
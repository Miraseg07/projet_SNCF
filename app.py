import os
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 
from pipelines.answer_query import process_full_query

app = Flask(__name__, static_folder="static")
CORS(app) 

# Fonction pour extraire dynamiquement la liste des gares pour le HTML
def get_stations_list():
    path = os.path.join("data_source", "gares-de-voyageurs.csv")
    if os.path.exists(path):
        try:
            df = pd.read_csv(path, sep=';', engine="python")
            if 'Nom_Gare' in df.columns:
                return sorted(df['Nom_Gare'].dropna().unique().tolist())
        except Exception as e:
            print(f" Erreur chargement liste gares: {e}")
    return ["Paris Gare du Nord", "Gare de Lyon", "Aix-en-Provence TGV"] # Liste de secours

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# Route pour envoyer la liste des gares au HTML au chargement
@app.route("/stations", methods=["GET"])
def stations():
    return jsonify(get_stations_list())

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        station = data.get("station", "").strip()
        question = data.get("question", "").strip()

        if not station or not question:
            return jsonify({"answer": "Veuillez choisir une gare et poser une question."}), 400

        answer = process_full_query(station, question)
        return jsonify({"answer": answer})

    except Exception as e:
        print(f" Erreur : {e}")
        return jsonify({"answer": f"Problème technique : {str(e)}"}), 500

if __name__ == "__main__":
    print(" Serveur Horizon AI prêt sur http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
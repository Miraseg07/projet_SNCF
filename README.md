# projet_SNCF
# Horizon AI : Système de Question-Réponse Augmenté (RAG) pour le Réseau Ferroviaire

## Introduction
Horizon AI est une application de démonstration technologique visant à améliorer l'accès aux informations voyageurs pour le réseau SNCF. En s'appuyant sur les dernières avancées en Intelligence Artificielle Générative, le projet propose une interface capable d'interpréter des requêtes complexes en langage naturel pour fournir des réponses précises, sourcées et actualisées.

## Architecture Technique : Le paradigme RAG
La principale innovation de ce projet réside dans son architecture **RAG (Retrieval-Augmented Generation)**. Contrairement aux modèles d'IA conversationnels standards qui s'appuient uniquement sur leurs connaissances pré-entraînées, Horizon AI connecte le Modèle de Langage (LLM) à des bases de données externes en temps réel.

### Avantages de l'approche RAG :
* **Élimination des hallucinations :** Le système ne génère des réponses qu'à partir des données fournies en contexte.
* **Fiabilité factuelle :** Les informations sont ancrées dans les référentiels officiels de l'entreprise.
* **Traçabilité :** Chaque réponse est issue d'une analyse sémantique de documents structurés (CSV).

## Exploitation de l'Open Data SNCF
La pertinence du système repose sur l'ingestion de jeux de données réels provenant du portail **SNCF Open Data**. L'application traite et croise plusieurs sources d'informations :
* **Référentiel Gares et Connexions :** Données géographiques et nomenclatures officielles.
* **Accessibilité :** Inventaire des équipements pour les Personnes à Mobilité Réduite (PMR).
* **Services et Confort :** Disponibilité du Wi-Fi, des services d'attente et des commerces en gare.
* **Horaires :** Plages de fonctionnement des infrastructures ferroviaires.

## Stack Technologique
* **Moteur d'IA :** Google Gemini Pro (LLM).
* **Backend :** Python 3.x / Flask pour la gestion des API et de la logique métier.
* **Data Processing :** Bibliothèque Pandas pour le filtrage et l'interrogation sémantique des jeux de données.
* **Frontend :** HTML5, CSS3 et JavaScript (ES6+) pour une interface utilisateur asynchrone et réactive.
* **Déploiement :** Infrastructure Cloud via Render, configurée pour une intégration continue (CI/CD).

## Fonctionnalités Avancées
* **Traitement du langage naturel (NLP) :** Compréhension des intentions utilisateurs sans nécessiter de mots-clés spécifiques.
* **Recherche contextuelle :** Capacité du système à identifier les équipements spécifiques d'une gare choisie parmi des milliers d'entrées.
* **Sécurisation de l'API :** Gestion des clés de service via des variables d'environnement pour une sécurité optimale en production.

## Guide d'Installation et Configuration
1. **Clonage du dépôt :** `git clone https://github.com/Miraseg07/projet_SNCF.git`
2. **Installation des dépendances :** `pip install -r requirements.txt`
3. **Configuration système :** Définir la variable d'environnement `GOOGLE_API_KEY` avec une clé valide.
4. **Exécution :** Lancer l'application via `python app.py`.

## Accès au Service
* **Lien de production :** https://projet-sncf.onrender.com/
* **Auteur :** [Ton Nom]

---
*Ce projet constitue une preuve de concept (PoC) dédiée à l'exploration des synergies entre l'ingénierie des données et l'intelligence artificielle appliquée aux services publics.*

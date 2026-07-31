# AMENet Chatbot Assistant

Prototype de chatbot bancaire réalisé dans le cadre d'un stage ingénieur chez **AMEN Bank**.

L'objectif du projet est de concevoir et développer un assistant conversationnel capable de répondre à des demandes bancaires courantes dans un environnement entièrement simulé. Le prototype s'appuie sur une API bancaire fictive, une interface de chat et un module RAG pour les questions documentaires.

## Important

Ce projet est un prototype académique/de stage.

- Aucune donnée client réelle n'est utilisée.
- Aucune opération bancaire réelle n'est exécutée.
- Les données bancaires présentes dans le projet sont fictives.
- Les documents utilisés pour le module documentaire proviennent de ressources publiques et de l'analyse de la démo AMENet.
- Les actions sensibles sont uniquement enregistrées dans un environnement de simulation.

## Fonctionnalités principales

Le prototype permet notamment de :

- consulter un solde fictif ;
- afficher des mouvements bancaires fictifs ;
- préparer un virement simulé ;
- faire une demande d'opposition sur carte ;
- demander un chéquier ;
- demander un document bancaire ;
- simuler un crédit ;
- préparer un message vers l'agence ou le support ;
- répondre à des questions documentaires grâce à un module RAG.

Les actions sensibles, comme les virements, l'opposition sur carte ou les demandes de documents, nécessitent une confirmation explicite de l'utilisateur avant d'être enregistrées dans l'environnement de simulation.

## Architecture générale

Le projet est organisé autour de trois blocs principaux :

```text
frontend Streamlit
        |
        v
backend FastAPI
        |
        +-- services bancaires simulés
        |
        +-- détection d'intentions
        |
        +-- module RAG documentaire
```

Le backend expose notamment :

```text
GET  /health
POST /chat
POST /rag/search
```

## Stack technique

- Python 3.12
- FastAPI
- Streamlit
- Pydantic
- pytest
- ChromaDB
- sentence-transformers
- PyMuPDF
- requests
- pandas / numpy

Le modèle d'embeddings utilisé pour le RAG est :

```text
intfloat/multilingual-e5-small
```

## Structure du projet

```text
backend/
  app/
    api/          Routes FastAPI
    core/         Configuration globale
    rag/          Pipeline RAG : loaders, chunker, embeddings, indexer, retriever
    services/     Logique métier : chatbot, intents, services bancaires simulés
    models/       Modèles métier
  tests/          Tests unitaires et API

frontend/
  streamlit_app.py

data/
  mock/           Données bancaires fictives
  raw/            Captures AMENet et documents publics
  extracted/      Textes extraits des documents
  processed/      Documents et chunks préparés pour le RAG
  vectorstore/    Index Chroma local, non versionné

docs/
  analyse_amenet.md
  cahier_des_charges.md
  choix_techniques.md
  architecture.md
  planning.md

evaluation/
  Jeux de questions et supports d'évaluation

scripts/
  ingest_rag_sources.py
  build_rag_index.py
  query_rag.py
```

## Installation

Cloner le dépôt puis se placer dans le dossier du projet :

```bash
git clone https://github.com/AdamBouzid0/amen-bank-chatbot.git
cd amen-bank-chatbot
```

Créer et activer un environnement virtuel :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Préparation du module RAG

Le dossier `data/vectorstore/` n'est pas versionné. Il faut donc reconstruire l'index localement avant d'utiliser les fonctionnalités RAG.

Lancer l'ingestion des sources :

```bash
python scripts/ingest_rag_sources.py
```

Construire l'index vectoriel Chroma :

```bash
python scripts/build_rag_index.py
```

Tester une recherche RAG en ligne de commande :

```bash
python scripts/query_rag.py "Comment faire opposition à une carte ?"
```

## Lancement du backend

Depuis la racine du projet, avec l'environnement virtuel activé :

```bash
uvicorn backend.app.main:app --reload
```

Le backend est ensuite disponible à l'adresse :

```text
http://127.0.0.1:8000
```

La documentation Swagger est disponible ici :

```text
http://127.0.0.1:8000/docs
```

## Lancement de l'interface Streamlit

Dans un deuxième terminal, avec l'environnement virtuel activé :

```bash
streamlit run frontend/streamlit_app.py
```

L'interface Streamlit permet de tester le chatbot avec deux clients fictifs.

## Exemples de requêtes

Questions bancaires simulées :

```text
Quel est mon solde ?
Affiche mes dernières opérations
Je veux faire un virement de 500 DT
Je veux bloquer ma carte qui termine par 4582
Je veux commander un chéquier
Je veux demander un relevé
Simule un crédit de 20000 DT sur 5 ans
```

Questions documentaires traitées par le RAG :

```text
Comment faire opposition à une carte ?
Comment commander un chéquier ?
Comment demander un document bancaire ?
Quels services sont disponibles sur AMENet ?
Quelles actions nécessitent une confirmation ?
```

## Exemple d'appel API

Appel direct à `/chat` :

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Comment faire opposition à une carte ?", "client_id": "C001"}'
```

Appel direct à `/rag/search` :

```bash
curl -X POST "http://127.0.0.1:8000/rag/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Comment faire opposition à une carte ?", "top_k": 4}'
```

## Tests

Lancer les tests avec l'environnement virtuel activé :

```bash
python -m pytest
```

## Fonctionnement du chatbot

Le chatbot distingue deux types de demandes :

### 1. Demandes actionnables

Exemple :

```text
Je veux bloquer ma carte qui termine par 4582
```

Le chatbot détecte une intention d'action sensible et demande une confirmation avant d'enregistrer l'action simulée.

### 2. Questions informationnelles

Exemple :

```text
Comment faire opposition à une carte ?
```

Le chatbot interroge le module RAG et retourne une réponse basée sur les documents/chunks retrouvés, avec les sources associées.

## Limites actuelles

- Le projet utilise uniquement des données fictives.
- Les actions bancaires ne sont pas connectées à un système bancaire réel.
- Le module RAG repose sur un index local Chroma.
- Les réponses documentaires sont basées sur les passages récupérés, sans génération avancée par LLM externe.
- L'authentification, la gestion fine des droits et la sécurité production ne sont pas encore implémentées.
- L'interface Streamlit est une interface de démonstration.

## Objectif du prototype

Ce projet vise à démontrer la faisabilité d'un assistant bancaire capable de :

- comprendre des demandes simples ;
- distinguer information et action ;
- sécuriser les opérations sensibles par confirmation ;
- fournir des réponses documentaires avec sources ;
- offrir une base technique extensible pour un futur chatbot bancaire plus complet.

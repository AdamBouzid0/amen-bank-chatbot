# Amen Bank Chatbot Assistant

## Description

Ce projet est réalisé dans le cadre d'un stage ingénieur chez AMEN BANK.  
L'objectif est de développer un prototype de chatbot assistant bancaire capable de répondre à des questions générales, de simuler l'accès à certaines données bancaires et d'accompagner l'utilisateur dans quelques opérations courantes.

Le prototype est développé sans accès aux données bancaires réelles. Il repose sur :
- une analyse de la démo AMENet ;
- une base de données fictive ;
- des API bancaires simulées ;
- un module de recherche documentaire pour les questions générales ;
- une interface conversationnelle.

## Objectifs

- Analyser les principaux parcours utilisateurs d'AMENet.
- Concevoir une architecture de chatbot bancaire.
- Développer un backend avec des services bancaires simulés.
- Intégrer un module RAG pour les questions générales.
- Mettre en place des mécanismes de confirmation pour les actions sensibles.
- Tester et évaluer la qualité des réponses.

## Stack envisagée

- Python
- FastAPI
- Streamlit
- ChromaDB
- LangChain ou LlamaIndex
- SQLite ou PostgreSQL
- Docker
- pytest

## Structure du projet

```text
backend/      API principale et logique métier
frontend/     Interface chatbot
data/         Données brutes, données simulées et base documentaire
docs/         Analyse, cahier des charges et documentation
evaluation/   Jeux de test et résultats
notebooks/    Expérimentations
report/       Figures et éléments pour le rapport
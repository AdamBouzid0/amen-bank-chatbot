# Choix techniques du projet

## 1. Objectif du document

Ce document présente les choix techniques envisagés pour le développement du prototype de chatbot assistant bancaire.  
L'objectif est de justifier les technologies utilisées en fonction du contexte du stage, des contraintes du projet et des fonctionnalités attendues.

Le projet ne disposant pas d'un accès aux données bancaires réelles ni aux API internes, la solution sera construite autour d'un environnement simulé, avec des données fictives et des API bancaires mockées.

## 2. Contraintes du projet

Les principales contraintes techniques sont les suivantes :

- absence d'accès aux systèmes bancaires internes ;
- absence de données client réelles ;
- nécessité de travailler avec des données fictives ;
- besoin d'un prototype fonctionnel et démontrable ;
- architecture extensible en cas d'intégration future avec de vraies API ;
- nécessité de séparer les questions générales, les consultations de données et les actions sensibles ;
- attention particulière à la sécurité et à la confidentialité.

## 3. Langage principal : Python

Python est retenu comme langage principal du projet.

Ce choix est justifié par :

- sa simplicité de développement ;
- sa richesse en bibliothèques pour l'intelligence artificielle ;
- son écosystème mature pour les API web ;
- sa compatibilité avec les outils de RAG, d'embeddings et de traitement de données ;
- sa rapidité pour construire un prototype fonctionnel.

## 4. Backend : FastAPI

Le backend du chatbot sera développé avec FastAPI.

FastAPI permettra de construire une API claire et modulaire pour gérer :

- les messages envoyés au chatbot ;
- les consultations de solde ;
- les recherches de transactions ;
- les actions bancaires simulées ;
- les demandes de documents ;
- les demandes de chéquier ;
- les oppositions carte ;
- la simulation de crédit.

FastAPI est retenu car il permet de développer rapidement des endpoints REST tout en gardant une structure propre et testable.

## 5. Frontend : Streamlit

Pour la première version du prototype, Streamlit est retenu pour construire l'interface utilisateur.

Ce choix est justifié par :

- la rapidité de développement ;
- la simplicité de création d'une interface de chatbot ;
- la possibilité de tester facilement les fonctionnalités ;
- l'adaptation aux prototypes internes et démonstrateurs.

Une interface plus avancée en React pourra être envisagée comme amélioration future si le temps le permet.

## 6. Données simulées : fichiers JSON

Les données bancaires fictives seront d'abord stockées dans des fichiers JSON.

Les fichiers prévus sont :

- clients.json ;
- accounts.json ;
- transactions.json ;
- cards.json ;
- beneficiaries.json.

Cette solution est suffisante pour une première version du prototype. Elle permet de simuler des données bancaires sans mettre en place immédiatement une base de données complète.

Une base SQLite ou PostgreSQL pourra être envisagée dans une version plus avancée.

## 7. API bancaire simulée

En l'absence d'accès aux API internes d'AMEN BANK, une API bancaire simulée sera développée.

Cette API permettra de reproduire les comportements suivants :

- consultation du solde ;
- consultation des transactions ;
- recherche de mouvements ;
- préparation de virement ;
- opposition carte ;
- recharge carte prépayée ;
- demande de chéquier ;
- demande de document ;
- simulation de crédit.

L'objectif est de séparer la logique conversationnelle du chatbot de la logique bancaire.  
Ainsi, dans une future intégration, les fonctions simulées pourraient être remplacées par de vraies API internes.

## 8. RAG pour les questions générales

Le RAG sera utilisé pour répondre aux questions générales sur les services bancaires et sur l'utilisation d'AMENet.

Le RAG ne sera pas utilisé pour les données personnelles du client.

Cette séparation est importante :

- les questions générales peuvent être traitées à partir d'une base documentaire ;
- les données client doivent provenir d'une source structurée ;
- le modèle ne doit pas inventer un solde, une transaction ou une opération bancaire.

## 9. Base vectorielle : ChromaDB

ChromaDB est envisagé comme base vectorielle pour le module RAG.

Elle permettra de stocker les embeddings des documents et de retrouver les passages pertinents lorsqu'un utilisateur pose une question générale.

ChromaDB est adaptée au prototype car elle est simple à installer, facile à utiliser localement et suffisante pour une première version.

## 10. Framework RAG : LangChain ou LlamaIndex

Deux options sont envisagées pour construire le pipeline RAG :

- LangChain ;
- LlamaIndex.

Le choix final pourra être fait après quelques tests.

LangChain est intéressant pour sa flexibilité et son intégration avec différents modèles, outils et bases vectorielles.  
LlamaIndex est intéressant pour la construction rapide de systèmes de recherche documentaire.

Dans une première version, LangChain pourra être utilisé pour structurer le pipeline RAG.

## 11. Modèle de langage

Le choix du modèle de langage dépendra des contraintes de l'environnement de stage.

Deux options sont possibles :

### Modèle cloud

Un modèle cloud peut offrir de bonnes performances, mais pose des questions de confidentialité.  
Il ne doit pas recevoir de données bancaires sensibles.

### Modèle local

Un modèle local permet un meilleur contrôle des données, mais peut demander davantage de ressources matérielles.

Dans le prototype, les données personnelles étant fictives, l'utilisation d'un modèle externe peut être envisagée pour les tests, sous réserve de validation par l'encadrement.

## 12. Tests : pytest

La bibliothèque pytest sera utilisée pour tester les fonctionnalités principales.

Les tests concerneront notamment :

- la récupération du solde ;
- le filtrage des transactions ;
- la validation d'un montant ;
- la préparation d'un virement ;
- le blocage simulé d'une carte ;
- la simulation de crédit ;
- la détection de demandes hors périmètre.

## 13. Gestion de version : Git

Git est utilisé pour versionner le projet.

Les commits permettront de suivre l'évolution du projet :

- mise en place de la structure ;
- analyse de l'existant ;
- cahier des charges ;
- choix techniques ;
- implémentation des API ;
- ajout de l'interface ;
- tests et corrections.

## 14. Environnement de développement

L'environnement de développement prévu est le suivant :

- VS Code ;
- WSL Ubuntu ;
- Python 3.11 ou supérieur ;
- environnement virtuel Python ;
- Git ;
- navigateur web pour tester la démo AMENet ;
- Overleaf pour le rapport.

## 15. Choix retenus pour la première version

Pour la première version du prototype, les choix suivants sont retenus :

| Élément | Choix retenu |
|---|---|
| Langage | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Données simulées | JSON |
| RAG | LangChain |
| Base vectorielle | ChromaDB |
| Tests | pytest |
| Versioning | Git |
| Rapport | Overleaf |

## 16. Conclusion

Les choix techniques retenus privilégient la simplicité, la rapidité de prototypage et l'extensibilité.  
L'objectif est de construire une première version fonctionnelle du chatbot, sans dépendre des systèmes bancaires réels, tout en gardant une architecture qui pourra évoluer vers une intégration plus complète.
# Architecture technique - Chatbot assistant bancaire AMENet

## 1. Objectif du document

Ce document présente l'architecture technique envisagée pour le prototype de chatbot assistant bancaire inspiré de la démo AMENet.

L'objectif est de définir une architecture claire, modulaire et extensible, capable de fonctionner sans accès aux systèmes bancaires réels. Le chatbot reposera donc sur des données fictives, des API simulées et, pour les questions générales, un module de recherche documentaire de type RAG.

Cette architecture doit permettre de démontrer les principaux parcours utilisateurs tout en respectant les contraintes du contexte bancaire : confidentialité, sécurité, confirmation des actions sensibles et fiabilité des réponses.

---

## 2. Principes d'architecture

L'architecture du projet repose sur plusieurs principes.

### 2.1 Séparation des responsabilités

Le chatbot ne doit pas mélanger toutes les logiques dans un seul bloc. Les responsabilités sont séparées entre :

- l'interface utilisateur ;
- le backend ;
- le routeur d'intention ;
- les services bancaires simulés ;
- le module RAG ;
- les outils d'action bancaire ;
- les données fictives ;
- les tests et l'évaluation.

Cette séparation permet de rendre le projet plus lisible, plus maintenable et plus facilement extensible.

### 2.2 Séparation entre information et action

Une question informationnelle et une action bancaire ne doivent pas être traitées de la même manière.

Exemple :

- « Comment faire opposition à ma carte ? » est une question d'information.
- « Bloque ma carte » est une demande d'action sensible.

Le chatbot doit donc distinguer :

- les questions générales ;
- les demandes de consultation ;
- les actions sensibles ;
- les demandes hors périmètre.

### 2.3 Utilisation de données simulées

Le projet ne dispose pas d'un accès aux données bancaires réelles ni aux API internes d'AMEN BANK. Les données clients, comptes, transactions, cartes, bénéficiaires et demandes bancaires seront donc simulées.

Cette approche permet de tester l'architecture et les parcours utilisateurs sans manipuler de données sensibles.

### 2.4 Extensibilité

L'architecture doit permettre, dans une évolution future, de remplacer les API simulées par de vraies API internes sans modifier entièrement le chatbot.

Le backend doit donc jouer le rôle d'une couche intermédiaire entre l'interface conversationnelle et les services bancaires.

---

## 3. Vue d'ensemble de l'architecture

L'architecture générale du prototype est la suivante :

```text
Utilisateur
   |
   v
Interface chatbot Streamlit
   |
   v
Backend FastAPI
   |
   v
Routeur d'intention
   |
   |--- Questions générales ---------> Module RAG
   |
   |--- Consultation bancaire -------> Services bancaires simulés
   |
   |--- Action bancaire sensible ----> Confirmation + outils bancaires simulés
   |
   |--- Simulation / calcul ---------> Module de simulation
   |
   |--- Messagerie ------------------> Génération de message structuré
   |
   |--- Hors périmètre --------------> Refus / redirection
```

---

## 4. Architecture en couches

Le système peut être organisé en plusieurs couches.

```text
+--------------------------------------------------+
| Interface utilisateur                            |
| Streamlit chatbot                                |
+--------------------------------------------------+
                      |
                      v
+--------------------------------------------------+
| API backend                                      |
| FastAPI routes : chat, banking, rag              |
+--------------------------------------------------+
                      |
                      v
+--------------------------------------------------+
| Couche services                                  |
| ChatService, IntentService, MockBankingService   |
+--------------------------------------------------+
                      |
                      v
+--------------------------------------------------+
| Couche métier / outils                           |
| Solde, transactions, virements, cartes, crédit   |
+--------------------------------------------------+
                      |
                      v
+--------------------------------------------------+
| Couche données                                   |
| JSON fictifs, documents, vector store            |
+--------------------------------------------------+
```

---

## 5. Composants principaux

### 5.1 Interface utilisateur

L'interface utilisateur sera développée avec Streamlit.

Elle permettra à l'utilisateur de :

- saisir un message en langage naturel ;
- visualiser la réponse du chatbot ;
- suivre l'historique de la conversation ;
- confirmer ou annuler une action sensible ;
- tester différents scénarios de démonstration.

Dans une première version, Streamlit est suffisant car l'objectif est de créer un prototype rapidement testable.

### 5.2 Backend FastAPI

Le backend FastAPI est le cœur de l'application.

Il expose les routes nécessaires pour :

- recevoir les messages du chatbot ;
- interroger les services bancaires simulés ;
- lancer le module RAG ;
- préparer les actions sensibles ;
- enregistrer les demandes simulées ;
- retourner une réponse structurée au frontend.

Les principaux fichiers concernés seront :

```text
backend/app/main.py
backend/app/api/chat_routes.py
backend/app/api/banking_routes.py
backend/app/api/rag_routes.py
```

### 5.3 Routeur d'intention

Le routeur d'intention a pour rôle d'identifier le type de demande utilisateur.

Exemples d'intentions :

| Intention | Exemple utilisateur | Traitement |
|---|---|---|
| general_question | Comment faire un virement ? | RAG |
| get_balance | Quel est mon solde ? | API simulée |
| get_transactions | Affiche mes dernières opérations | API simulée |
| prepare_transfer | Prépare un virement de 500 DT | Confirmation + API simulée |
| block_card | Je veux bloquer ma carte | Confirmation + API simulée |
| request_checkbook | Je veux commander un chéquier | API simulée |
| request_document | Je veux un relevé de compte | API simulée |
| simulate_credit | Simule un crédit de 20000 DT | Module de calcul |
| contact_support | Je n'arrive pas à me connecter | Génération de message |
| out_of_scope | Donne-moi le mot de passe d'un client | Refus |

Dans une première version, ce routeur peut être basé sur des règles simples et des mots-clés. Il pourra ensuite évoluer vers une classification plus avancée.

### 5.4 Services bancaires simulés

Les services bancaires simulés reproduisent certains comportements observés dans la démo AMENet.

Ils permettent notamment de :

- consulter le solde ;
- rechercher des mouvements ;
- afficher les dernières transactions ;
- préparer un virement ;
- faire opposition sur une carte ;
- demander un chéquier ;
- demander un document ;
- simuler un crédit ;
- enregistrer un message au support ou à l'agence.

Ces services n'exécutent aucune opération réelle. Ils manipulent uniquement des données fictives stockées localement.

Fichier principal :

```text
backend/app/services/mock_banking_service.py
```

### 5.5 Module RAG

Le module RAG est utilisé pour répondre aux questions générales sur les services bancaires et sur l'utilisation d'AMENet.

Le pipeline RAG est le suivant :

```text
Documents publics / notes internes simulées
   |
   v
Nettoyage et structuration
   |
   v
Découpage en chunks
   |
   v
Génération des embeddings
   |
   v
Stockage dans ChromaDB
   |
   v
Recherche des passages pertinents
   |
   v
Génération de réponse contextualisée
```

Les fichiers concernés seront :

```text
backend/app/rag/document_loader.py
backend/app/rag/chunker.py
backend/app/rag/embeddings.py
backend/app/rag/retriever.py
backend/app/rag/rag_chain.py
```

Le RAG ne sera pas utilisé pour les données personnelles simulées comme les soldes, les transactions ou les cartes.

### 5.6 Outils bancaires

Les outils bancaires représentent les actions spécifiques que le chatbot peut déclencher dans l'environnement simulé.

Exemples :

```text
balance_tool.py
transaction_tool.py
transfer_tool.py
card_tool.py
checkbook_tool.py
```

Ces outils peuvent être appelés par le service de chat après identification de l'intention.

---

## 6. Flux de traitement d'un message utilisateur

Lorsqu'un utilisateur envoie un message, le traitement suit les étapes suivantes :

```text
1. L'utilisateur saisit une question dans l'interface Streamlit.
2. Le frontend envoie le message au backend FastAPI.
3. Le backend transmet le message au ChatService.
4. Le ChatService appelle l'IntentService.
5. L'IntentService identifie l'intention.
6. Selon l'intention :
   - le module RAG est appelé ;
   - ou une API simulée est appelée ;
   - ou une confirmation est demandée ;
   - ou une réponse de refus est générée.
7. Le backend retourne une réponse structurée.
8. Le frontend affiche la réponse à l'utilisateur.
```

---

## 7. Exemples de flux

### 7.1 Flux : consultation du solde

```text
Utilisateur : Quel est mon solde ?

Frontend
   -> POST /chat
Backend
   -> IntentService : get_balance
   -> MockBankingService.get_balance(client_id)
   -> Réponse structurée

Chatbot : Votre compte courant se terminant par 3456 présente un solde de 3 250,750 DT.
```

### 7.2 Flux : question générale

```text
Utilisateur : Comment faire opposition à une carte ?

Frontend
   -> POST /chat
Backend
   -> IntentService : general_question
   -> RAG Retriever
   -> Génération de réponse contextualisée

Chatbot : Pour faire opposition à une carte, vous devez sélectionner la carte concernée, indiquer le motif, puis confirmer la demande.
```

### 7.3 Flux : action sensible

```text
Utilisateur : Bloque ma carte.

Frontend
   -> POST /chat
Backend
   -> IntentService : block_card
   -> Recherche des cartes du client
   -> Demande de confirmation

Chatbot : Vous souhaitez faire opposition sur la carte se terminant par 4582. Confirmez-vous ?

Utilisateur : Oui.

Backend
   -> MockBankingService.block_card(card_id)
   -> Enregistrement de la demande simulée

Chatbot : Votre demande d'opposition a été enregistrée dans l'environnement de simulation.
```

---

## 8. Gestion des actions sensibles

Les actions sensibles doivent suivre un mécanisme en deux étapes.

```text
Étape 1 : préparation de l'action
Étape 2 : confirmation explicite de l'utilisateur
```

Actions concernées :

- virement compte à compte ;
- virement vers bénéficiaire ;
- opposition carte ;
- recharge carte prépayée ;
- demande de document ;
- demande de chéquier ;
- demande de carte.

Le chatbot ne doit jamais exécuter directement une action sensible après une seule phrase utilisateur.

---

## 9. Structure des données simulées

Les données simulées sont stockées dans le dossier :

```text
data/mock/
```

Les fichiers prévus sont :

```text
clients.json
accounts.json
transactions.json
cards.json
beneficiaries.json
```

Des fichiers supplémentaires pourront être ajoutés ensuite :

```text
requests.json
transfers.json
messages.json
credit_simulations.json
```

### 9.1 Exemple de modèle Client

```json
{
  "client_id": "C001",
  "name": "Société Démo SARL",
  "client_type": "entreprise",
  "agency": "Agence Tunis Centre",
  "subscriber_number": "ABN-0001"
}
```

### 9.2 Exemple de modèle Compte

```json
{
  "account_id": "ACC001",
  "client_id": "C001",
  "masked_account_number": "**** **** **** 3456",
  "label": "Compte courant entreprise",
  "currency": "TND",
  "balance": 3250.750,
  "balance_date": "2026-05-12"
}
```

### 9.3 Exemple de modèle Transaction

```json
{
  "transaction_id": "TX001",
  "account_id": "ACC001",
  "date": "2026-05-10",
  "label": "Paiement fournisseur",
  "amount": -500.000,
  "direction": "debit",
  "category": "Fournisseurs"
}
```

---

## 10. API prévue

### 10.1 Routes principales

| Route | Méthode | Rôle |
|---|---|---|
| /chat | POST | Envoyer un message au chatbot |
| /banking/accounts | GET | Lister les comptes fictifs |
| /banking/balance/{account_id} | GET | Consulter le solde |
| /banking/transactions/{account_id} | GET | Consulter les transactions |
| /banking/transfer/prepare | POST | Préparer un virement |
| /banking/card/block | POST | Simuler une opposition carte |
| /banking/checkbook/request | POST | Demander un chéquier |
| /banking/document/request | POST | Demander un document |
| /banking/credit/simulate | POST | Simuler un crédit |
| /rag/query | POST | Poser une question au module RAG |

### 10.2 Réponse standard du chatbot

Le backend retournera une réponse structurée sous la forme suivante :

```json
{
  "message": "Réponse affichée à l'utilisateur",
  "intent": "get_balance",
  "requires_confirmation": false,
  "data": {},
  "sources": [],
  "error": null
}
```

Pour une action sensible :

```json
{
  "message": "Vous souhaitez effectuer un virement de 500 DT. Confirmez-vous ?",
  "intent": "prepare_transfer",
  "requires_confirmation": true,
  "pending_action": {
    "type": "transfer",
    "amount": 500,
    "currency": "TND"
  },
  "error": null
}
```

---

## 11. Sécurité et confidentialité

Même si les données sont fictives, l'architecture doit intégrer des principes de sécurité.

### 11.1 Masquage des données

Les numéros de compte et de carte doivent être masqués.

Exemple :

```text
Carte se terminant par 4582
Compte se terminant par 3456
```

### 11.2 Refus des demandes dangereuses

Le chatbot doit refuser certaines demandes.

Exemples :

- demander le numéro complet d'une carte ;
- demander le mot de passe d'un client ;
- exécuter une action sans confirmation ;
- donner une information non disponible ;
- inventer une condition bancaire non documentée.

### 11.3 Limitation du RAG

Le RAG ne doit pas être utilisé pour répondre à des questions sur les données personnelles du client.

### 11.4 Journalisation

Les actions simulées peuvent être enregistrées pour faciliter les tests :

- type d'action ;
- date ;
- client fictif ;
- statut ;
- message associé.

---

## 12. Organisation du code

La structure prévue du backend est la suivante :

```text
backend/app/
├── main.py
├── api/
│   ├── chat_routes.py
│   ├── banking_routes.py
│   └── rag_routes.py
├── core/
│   ├── config.py
│   └── security.py
├── models/
│   ├── client.py
│   ├── account.py
│   ├── transaction.py
│   └── card.py
├── services/
│   ├── mock_banking_service.py
│   ├── chat_service.py
│   └── intent_service.py
├── rag/
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── rag_chain.py
├── tools/
│   ├── balance_tool.py
│   ├── transaction_tool.py
│   ├── transfer_tool.py
│   ├── card_tool.py
│   └── checkbook_tool.py
└── utils/
    ├── logger.py
    └── text_cleaning.py
```

---

## 13. Tests prévus

Les tests seront organisés dans :

```text
backend/tests/
```

Les tests prioritaires sont :

- récupération du solde ;
- filtrage des transactions ;
- recherche par période ;
- validation du montant d'un virement ;
- confirmation obligatoire des actions sensibles ;
- opposition carte simulée ;
- simulation de crédit ;
- refus des demandes hors périmètre.

---

## 14. Évolutions possibles

L'architecture proposée pourra évoluer vers :

- une interface React plus avancée ;
- une base PostgreSQL ;
- une authentification réelle ;
- une connexion avec des API internes ;
- un modèle local pour réduire les risques de confidentialité ;
- un module de monitoring ;
- une évaluation automatique des réponses ;
- une gestion multilingue français / arabe.

---

## 15. Conclusion

L'architecture proposée permet de construire un prototype de chatbot bancaire réaliste, sécurisé et extensible. Elle repose sur une séparation claire entre les questions générales, les données bancaires simulées et les actions sensibles.

Cette approche est adaptée au contexte du stage, car elle permet de développer un démonstrateur complet sans accès aux systèmes bancaires réels, tout en préparant une éventuelle intégration future avec les services internes d'AMEN BANK.

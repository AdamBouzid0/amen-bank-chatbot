# Cahier des charges - Chatbot assistant bancaire AMENet

## 1. Contexte du projet

Le projet consiste à concevoir et développer un prototype de chatbot assistant bancaire inspiré des fonctionnalités observées dans la démo AMENet d'AMEN BANK.

L'objectif n'est pas de connecter directement le chatbot aux systèmes bancaires réels, mais de construire une solution autonome, réaliste et extensible. Le prototype reposera sur l'analyse de la démo AMENet, sur des données fictives et sur des API simulées reproduisant certains services bancaires.

Cette approche permet de démontrer les fonctionnalités principales d'un assistant bancaire tout en évitant la manipulation de données sensibles.

## 2. Objectifs du chatbot

Le chatbot doit permettre à un utilisateur de dialoguer en langage naturel avec un assistant bancaire capable de :

- répondre à des questions générales sur les services AMENet ;
- consulter des informations bancaires simulées ;
- rechercher des mouvements sur un compte fictif ;
- préparer certaines opérations bancaires dans un environnement de simulation ;
- aider l'utilisateur à rédiger des demandes ou messages ;
- fournir des réponses claires, sécurisées et cohérentes.

## 3. Utilisateurs cibles

La démo AMENet observée semble principalement orientée vers les clients professionnels ou entreprises, notamment à travers les fonctionnalités suivantes :

- comptes d'entreprise ;
- virements de masse ;
- monétique TPE ;
- fichiers CFONB ;
- opérations de bancaire étranger ;
- lettres de crédit ;
- messagerie avec agence ou support.

Le prototype ciblera donc principalement un utilisateur de type client professionnel ou client entreprise, tout en conservant des fonctionnalités compréhensibles pour un client particulier.

## 4. Périmètre fonctionnel du MVP

Le MVP du chatbot sera organisé autour de quatre blocs fonctionnels.

### 4.1 Consultation bancaire

Le chatbot doit permettre de consulter des données bancaires fictives.

| Fonctionnalité | Exemple de demande | Priorité |
|---|---|---|
| Consulter le solde | Quel est le solde de mon compte ? | Haute |
| Voir les dernières transactions | Affiche mes dernières opérations | Haute |
| Rechercher des mouvements | Montre-moi les opérations entre le 1er et le 30 mai | Haute |
| Résumer les dépenses | Combien ai-je dépensé ce mois-ci ? | Haute |
| Voir l'historique des virements | Affiche mes derniers virements | Moyenne |

### 4.2 Actions bancaires simulées

Le chatbot doit pouvoir préparer des actions bancaires sans jamais les exécuter réellement.

| Fonctionnalité | Exemple de demande | Priorité |
|---|---|---|
| Virement compte à compte | Fais un virement de 250 DT vers mon autre compte | Haute |
| Virement vers bénéficiaire | Prépare un virement de 500 DT à mon fournisseur | Haute |
| Opposition sur carte | Je veux bloquer ma carte | Haute |
| Recharge carte prépayée | Recharge ma carte prépayée de 100 DT | Moyenne |
| Commande de chéquier | Je veux commander un chéquier | Haute |
| Demande de document | Je veux demander un relevé de compte | Haute |
| Demande de carte | Je veux demander une nouvelle carte | Moyenne |

Toutes les actions sensibles doivent nécessiter une confirmation explicite de l'utilisateur.

### 4.3 Assistance et messagerie

Le chatbot doit aider l'utilisateur à formuler des messages ou demandes.

| Fonctionnalité | Exemple de demande | Priorité |
|---|---|---|
| Message à l'agence | Rédige un message à mon agence | Haute |
| Message au support | Je veux signaler un problème de connexion | Moyenne |
| Reformulation d'une demande | Aide-moi à écrire une demande claire | Moyenne |

### 4.4 Simulation et aide à la décision

Le chatbot doit proposer des fonctionnalités simples de calcul ou d'analyse.

| Fonctionnalité | Exemple de demande | Priorité |
|---|---|---|
| Simulation de crédit | Simule un crédit de 20000 DT sur 5 ans | Haute |
| Estimation mensualité | Combien je paierai par mois ? | Haute |
| Analyse des dépenses | Résume mes dépenses par catégorie | Moyenne |

## 5. Fonctionnalités hors périmètre

Les fonctionnalités suivantes ne seront pas développées dans la première version :

- connexion aux systèmes internes d'AMEN BANK ;
- accès aux données réelles des clients ;
- exécution réelle de virements ;
- signature électronique réelle ;
- authentification bancaire forte réelle ;
- validation par SMS ou application mobile ;
- virement de masse réel ;
- transfert international réel ;
- génération réelle de fichiers CFONB ;
- intégration directe à AMENet ;
- déploiement en production.

Ces éléments pourront être présentés comme perspectives d'évolution.

## 6. Contraintes techniques

Le projet devra respecter les contraintes suivantes :

- développement d'un prototype autonome ;
- utilisation de données fictives ;
- séparation entre interface conversationnelle et logique bancaire ;
- architecture modulaire ;
- possibilité de remplacer les API simulées par de vraies API dans le futur ;
- code versionné avec Git ;
- documentation technique claire ;
- tests sur les fonctionnalités principales.

## 7. Contraintes de sécurité

Même si le prototype utilise des données fictives, il doit intégrer des principes de sécurité adaptés au contexte bancaire :

- ne jamais afficher de numéro de carte complet ;
- masquer les informations sensibles ;
- demander une confirmation pour les actions sensibles ;
- refuser les demandes dangereuses ou hors périmètre ;
- distinguer les questions d'information des demandes d'action ;
- journaliser les actions simulées ;
- ne pas stocker les données personnelles dans la base vectorielle du RAG ;
- éviter les réponses inventées sur des informations bancaires sensibles.

## 8. Données simulées nécessaires

Le prototype nécessitera plusieurs types de données fictives.

### 8.1 Clients

Chaque client fictif devra contenir :

- identifiant client ;
- nom ;
- type de client : particulier ou entreprise ;
- agence ;
- numéro abonné fictif.

### 8.2 Comptes

Chaque compte devra contenir :

- identifiant du compte ;
- numéro de compte masqué ;
- type de compte ;
- devise ;
- solde ;
- date du solde.

### 8.3 Transactions

Chaque transaction devra contenir :

- date ;
- libellé ;
- montant ;
- sens : débit ou crédit ;
- catégorie ;
- compte associé.

### 8.4 Cartes

Chaque carte devra contenir :

- identifiant carte ;
- numéro masqué ;
- type de carte ;
- statut ;
- compte associé.

### 8.5 Bénéficiaires

Chaque bénéficiaire devra contenir :

- identifiant bénéficiaire ;
- nom ou raison sociale ;
- banque ;
- numéro de compte ou RIB fictif.

### 8.6 Demandes bancaires

Le système devra stocker les demandes simulées :

- demande de chéquier ;
- demande de document ;
- demande de carte ;
- opposition carte ;
- demande de crédit ;
- message agence ou support.

## 9. Architecture fonctionnelle attendue

L'architecture fonctionnelle du chatbot sera la suivante :

```text
Utilisateur
   |
Interface chatbot
   |
Backend FastAPI
   |
Routeur d'intention
   |--- Questions générales --> Module RAG
   |--- Consultation compte --> API bancaire simulée
   |--- Action bancaire --> Confirmation + API simulée
   |--- Message/support --> Génération assistée
   |--- Hors périmètre --> Refus ou redirection
```

## 10. Critères de réussite

Le projet sera considéré comme réussi si :

- le chatbot répond correctement aux principales questions prévues ;
- les données affichées proviennent des données fictives et ne sont pas inventées ;
- les actions sensibles nécessitent une confirmation ;
- le chatbot refuse les demandes hors périmètre ;
- l'architecture est claire et extensible ;
- le code est documenté ;
- un jeu de tests permet d'évaluer les réponses ;
- une démonstration finale permet de montrer plusieurs parcours réalistes.

## 11. Scénarios de démonstration prévus

La démonstration finale pourra inclure les scénarios suivants.

### Scénario 1 : Consultation du solde

L'utilisateur demande le solde de son compte courant.
Le chatbot identifie le client fictif, récupère le compte correspondant et affiche le solde.

### Scénario 2 : Recherche de mouvements

L'utilisateur demande les opérations réalisées sur une période donnée.
Le chatbot filtre les transactions fictives et affiche un résumé.

### Scénario 3 : Virement vers bénéficiaire

L'utilisateur demande un virement vers un fournisseur.
Le chatbot collecte les informations nécessaires, reformule la demande et exige une confirmation.

### Scénario 4 : Opposition carte

L'utilisateur demande le blocage d'une carte.
Le chatbot affiche uniquement les cartes masquées, demande la confirmation puis enregistre l'opposition dans l'environnement simulé.

### Scénario 5 : Simulation de crédit

L'utilisateur demande une simulation de crédit.
Le chatbot calcule une mensualité approximative et présente le résultat.

### Scénario 6 : Message au support

L'utilisateur signale un problème de connexion.
Le chatbot aide à rédiger un message structuré au support.

## 12. Livrables attendus

Les livrables du projet sont :

- analyse de la démo AMENet ;
- cahier des charges ;
- architecture technique ;
- données fictives ;
- backend avec API simulées ;
- interface chatbot ;
- module RAG pour les questions générales ;
- module de tests ;
- rapport de stage ;
- démonstration finale.

## 13. Conclusion

Ce cahier des charges définit le périmètre initial du chatbot assistant bancaire. Le prototype sera développé comme une solution autonome, fondée sur des données simulées et inspirée des parcours observés dans AMENet. Cette approche permet de construire une démonstration réaliste tout en respectant les contraintes liées à l'absence d'accès aux données bancaires réelles.

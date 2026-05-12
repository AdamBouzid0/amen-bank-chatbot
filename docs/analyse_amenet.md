# Analyse de la démo AMENet

## 1. Objectif de l'analyse

L'objectif de cette analyse est d'étudier l'interface de démonstration AMENet afin d'identifier les principales fonctionnalités bancaires proposées aux clients. Cette analyse sert de base pour définir les cas d'usage du chatbot assistant bancaire et construire un environnement de simulation réaliste.

Comme le projet ne dispose pas d'un accès aux données bancaires réelles ni aux API internes d'AMEN BANK, la démo AMENet est utilisée comme source d'observation pour comprendre les parcours utilisateurs, les objets métier manipulés et les opérations bancaires pouvant être adaptées sous forme conversationnelle.

Le projet sera donc conçu comme un prototype autonome : il ne se connectera pas aux systèmes bancaires réels, mais reproduira certains parcours à partir de données fictives et d'API simulées.

## 2. Périmètre de l'observation

L'analyse porte sur les fonctionnalités visibles dans la démo AMENet. L'interface observée semble principalement orientée vers des clients professionnels ou entreprises, notamment à travers la présence de comptes d'entreprise, de fonctionnalités TPE, de virements de masse, de fichiers CFONB, de modules de bancaire étranger et de lettres de crédit.

Les principaux modules observés sont :

- Compte ;
- Téléchargement ;
- Virement ;
- Monétique ;
- Bancaire Étranger ;
- Services ;
- Financement ;
- Change/Bourse ;
- Gestion de budget ;
- Messagerie.

## 3. Méthodologie

L'analyse consiste à parcourir les différents menus de la démo AMENet et à relever, pour chaque fonctionnalité observée :

- le nom du module ;
- la fonctionnalité proposée ;
- l'objectif utilisateur ;
- les champs ou données visibles ;
- la possibilité d'adaptation sous forme de chatbot ;
- la priorité pour le prototype.

Les captures d'écran réalisées sont conservées dans le dossier suivant :

```text
data/raw/amenet_observations/
```

## 4. Vue d'ensemble des modules AMENet

| Module | Rôle principal observé | Intérêt pour le chatbot |
|---|---|---|
| Compte | Consultation des comptes, soldes, mouvements et fichiers CFONB | Très utile pour les fonctionnalités de consultation bancaire simulée |
| Téléchargement | Accès à des documents bancaires et justificatifs | Utile pour guider l'utilisateur ou simuler une demande de document |
| Virement | Virements compte à compte, vers bénéficiaire, permanents ou de masse | Très utile pour les actions bancaires simulées avec confirmation |
| Monétique | TPE, cartes prépayées, cartes internationales et opposition carte | Utile pour les clients professionnels et les actions sensibles |
| Bancaire Étranger | Transferts internationaux et lettres de crédit | Intéressant mais complexe, plutôt hors MVP |
| Services | Chéquier, carte, document, main levée, promotion immobilière | Très utile pour les demandes bancaires simulées |
| Financement | Demande et simulation de crédit | Utile pour la simulation et l'aide à la décision |
| Change/Bourse | Cours SICAV et cours de bourse | Plutôt informationnel, priorité basse |
| Gestion de budget | Paramétrage, catégories, dépenses, revenus, état des dépenses | Utile pour l'analyse des dépenses avec données fictives |
| Messagerie | Messages à l'agence ou au support | Utile pour l'assistance et la génération de messages |

## 5. Fonctionnalités observées dans la démo AMENet

| Module | Fonctionnalité observée | Objectif utilisateur | Champs / données visibles | Adaptation chatbot | Priorité |
|---|---|---|---|---|---|
| Compte | Vue d'ensemble des comptes | Consulter les comptes disponibles et leurs soldes | N° de compte, libellé compte, date solde, devise, solde actuel, total solde TND | Oui, via données simulées | Haute |
| Compte | Recherche de mouvements | Rechercher des opérations bancaires selon plusieurs critères | N° de compte, type de mouvement, débit minimum, débit maximum, crédit minimum, crédit maximum, date début, date fin | Oui, via API simulée de recherche de transactions | Haute |
| Compte | Mouvements par opération | Afficher les mouvements liés à un compte | N° de compte, option d'affichage, tableau | Oui, via API simulée | Moyenne |
| Compte | CFONB par compte par période | Générer ou consulter un fichier bancaire sur une période | N° de compte, date début, date fin | Oui, plutôt en simulation ou explication | Basse |
| Compte | Historique CFONB par compte | Consulter l'historique des fichiers CFONB d'un compte | Liste des comptes | Oui, plutôt informationnel | Basse |
| Compte | Historique CFONB global | Consulter l'historique global des fichiers CFONB | Historique global | Oui, plutôt informationnel | Basse |
| Téléchargement | Swift / ouverture LC / transferts | Télécharger des documents bancaires liés aux opérations internationales | Swift, ouverture LC, transferts émis, transferts reçus | Oui, en explication ou simulation de téléchargement | Basse |
| Téléchargement | Avis d'opération | Télécharger un avis d'opération en PDF ou texte | Avis d'opération PDF, avis d'opération texte | Oui, simulation de demande de document | Moyenne |
| Téléchargement | Documents divers | Télécharger différents documents bancaires | Image des chèques, image des lettres de change, situation cartes, situation crédits, relevé de compte, échelle d'intérêts | Oui, comme assistant de navigation ou demande de document | Moyenne |
| Virement | Virement compte à compte | Effectuer un virement entre deux comptes du même client | Compte à débiter, devise, compte à créditer, montant, motif paiement, date d'exécution | Oui, avec confirmation obligatoire | Haute |
| Virement | Virement vers bénéficiaire | Effectuer un virement vers un bénéficiaire externe ou enregistré | Compte à débiter, devise, compte à créditer, montant, motif paiement, date d'exécution, bénéficiaire, nom/raison sociale, banque, numéro de compte | Oui, avec confirmation obligatoire | Haute |
| Virement | Virements à signer | Consulter ou valider les virements en attente de signature | Liste des virements à signer | Oui, en consultation simulée | Moyenne |
| Virement | Historique des virements | Consulter les anciens virements | Liste ou historique des virements | Oui, via API simulée | Moyenne |
| Virement | Virement de masse | Effectuer plusieurs virements groupés | Fichier ou liste de virements | Possible, mais complexe | Basse |
| Virement | Virement permanent compte à compte | Programmer un virement récurrent entre comptes | Jour d'exécution, périodicité, premier virement, dernier virement, compte à débiter, devise, compte à créditer, montant, motif paiement | Oui, plutôt en bonus | Moyenne |
| Virement | Virement permanent vers bénéficiaire | Programmer un virement récurrent vers un bénéficiaire | Bénéficiaire, périodicité, dates, montant, motif | Oui, plutôt en bonus | Moyenne |
| Virement | Modèles de virement | Utiliser des modèles de virement prédéfinis | Modèles enregistrés | Oui, en bonus | Basse |
| Monétique | Consultation mouvements TPE | Consulter les mouvements liés aux terminaux de paiement électronique | Affiliation, terminal, date début, date fin | Oui, pour client professionnel | Moyenne |
| Monétique | Recharge carte prépayée | Recharger une carte prépayée | Liste des comptes, N° carte, montant en DT, règle montant multiple de 10, maximum 500 DT | Oui, avec validation des règles métier | Haute |
| Monétique | Déblocage carte internationale | Demander le déblocage international d'une carte | Compte, N° carte, montant, période, pays, options piste/e-commerce | Oui, avec confirmation | Moyenne |
| Monétique | Opposition sur carte | Bloquer une carte bancaire | Compte, N° carte, motif opposition | Oui, avec confirmation forte | Haute |
| Bancaire Étranger | Transfert émis / ordre de virement | Préparer un transfert international | Compte, bénéficiaire, devise, montant, informations de transfert | Possible, mais plutôt bonus | Basse |
| Bancaire Étranger | Transferts émis à signer | Consulter les transferts internationaux à signer | Liste des transferts en attente | Oui, en consultation simulée | Basse |
| Bancaire Étranger | Historique des transferts émis | Consulter les transferts internationaux précédents | Liste des transferts | Oui, en consultation simulée | Basse |
| Bancaire Étranger | Lettre de crédit | Initier une lettre de crédit | Type crédit, compte principal, compte professionnel, taux de blocage proposé | Possible, mais complexe | Basse |
| Services | Fiche promoteur | Consulter une fiche promoteur liée à la promotion immobilière | N° de compte | Plutôt hors MVP | Basse |
| Services | Projets immobiliers | Consulter des projets immobiliers | Liste ou informations projet | Plutôt hors MVP | Basse |
| Services | Stock de terrains | Consulter le stock de terrains | Liste ou informations terrain | Hors MVP | Basse |
| Services | Commande de chéquier | Consulter ou créer une demande de chéquier | Liste des demandes, bouton nouvelle demande de chéquier ; aucun formulaire détaillé visible dans la démo | Oui, action simulée simple | Haute |
| Services | Demande de carte | Consulter ou créer une demande de carte bancaire | Liste des demandes, bouton nouvelle demande de carte ; aucun formulaire détaillé visible dans la démo | Oui, action simulée | Moyenne |
| Services | Demande de main levée | Créer une demande de main levée | Données de compte ou dossier, formulaire non détaillé dans les captures | Possible, mais hors MVP | Basse |
| Services | Demande de document | Consulter ou créer une demande de document bancaire | Liste des demandes, bouton nouvelle demande de document ; aucun formulaire détaillé visible dans la démo | Oui, action simulée | Haute |
| Financement | Demande de crédit | Créer une demande de crédit | Liste des demandes, bouton nouvelle demande de crédit | Oui, simulation de demande | Moyenne |
| Financement | Simulation crédit | Simuler un crédit | Nature du crédit, montant du crédit, durée de remboursement, revenu mensuel brut, mensualité, montant maximum du crédit, capacité d'emprunt | Oui, module de calcul | Haute |
| Change/Bourse | Cours SICAV | Consulter des valeurs SICAV | Type SICAV, date SICAV, valeur SICAV, export CSV/Excel/PDF | Oui, informationnel | Basse |
| Change/Bourse | Cours de bourse | Consulter les cours de bourse | Liste des cours | Oui, informationnel | Basse |
| Gestion de budget | Paramétrage de la période d'analyse | Choisir la période d'analyse des dépenses | Période d'analyse, exemple : 1 mois | Oui, pour résumé des dépenses | Moyenne |
| Gestion de budget | Gestion des catégories | Gérer les catégories de dépenses | Catégories | Oui, en bonus | Moyenne |
| Gestion de budget | Dépenses et revenus | Consulter les dépenses et revenus | Message d'indisponibilité dans la démo, module prévu pour analyse budgétaire | Oui, avec données fictives catégorisées | Haute |
| Gestion de budget | État des dépenses | Visualiser l'état des dépenses d'un compte | N° de compte, état des dépenses | Oui, avec résumé conversationnel | Haute |
| Messagerie | Rédiger un message à l'agence | Envoyer un message à l'agence bancaire | Expéditeur, agence destinataire, objet, message, numéro de téléphone, pièce jointe | Oui, génération assistée de message | Haute |
| Messagerie | Rédiger un message au support | Envoyer une demande d'assistance technique | Support, objet, nom, adresse, numéro abonné, téléphone, fax, système d'exploitation, navigateur, description du problème, fichier joint | Oui, génération assistée et classification du problème | Moyenne |
| Messagerie | Messages reçus | Consulter les messages reçus | Liste des messages reçus | Oui, consultation simulée | Basse |
| Messagerie | Messages envoyés | Consulter les messages envoyés | Liste des messages envoyés | Oui, consultation simulée | Basse |
| Messagerie | Messages en instance | Consulter les brouillons ou messages en attente | Liste des messages en instance | Oui, consultation simulée | Basse |
| Messagerie | Messages supprimés | Consulter les messages supprimés | Liste des messages supprimés | Oui, consultation simulée | Basse |

## 6. Analyse des parcours adaptés au chatbot

Les fonctionnalités observées ne présentent pas toutes le même intérêt pour un assistant conversationnel. Certaines sont très adaptées à une interaction en langage naturel, tandis que d'autres sont plus complexes ou nécessitent une intégration forte avec les systèmes internes.

Les fonctionnalités les plus adaptées au prototype sont :

1. la consultation du solde ;
2. la recherche de mouvements ;
3. l'affichage des dernières transactions ;
4. le résumé des dépenses ;
5. le virement compte à compte ;
6. le virement vers bénéficiaire ;
7. la recharge de carte prépayée ;
8. l'opposition sur carte ;
9. la commande de chéquier ;
10. la demande de document ;
11. la simulation de crédit ;
12. la rédaction d'un message à l'agence ou au support.

Ces fonctionnalités ont été retenues car elles correspondent à des demandes fréquentes, peuvent être formulées naturellement par un utilisateur et peuvent être simulées sans accès aux systèmes bancaires réels.

## 7. MVP retenu pour le chatbot

À partir de l'analyse de la démo AMENet, le prototype du chatbot sera construit autour de fonctionnalités réalistes, utiles et démontrables sans accès aux systèmes internes de la banque.

### 7.1 Fonctionnalités principales du MVP

| Fonctionnalité chatbot | Exemple de demande utilisateur | Source de données | Type |
|---|---|---|---|
| Consultation du solde | Quel est le solde de mon compte ? | Données fictives | Consultation |
| Recherche de mouvements | Affiche les opérations entre le 1er et le 30 mai | Données fictives | Consultation |
| Dernières transactions | Montre-moi mes dernières opérations | Données fictives | Consultation |
| Résumé des dépenses | Combien ai-je dépensé ce mois-ci ? | Transactions fictives catégorisées | Analyse |
| Virement compte à compte | Fais un virement de 250 DT vers mon autre compte | API simulée | Action sensible |
| Virement vers bénéficiaire | Prépare un virement de 500 DT à mon fournisseur | API simulée | Action sensible |
| Recharge carte prépayée | Recharge ma carte prépayée de 100 DT | API simulée | Action sensible |
| Opposition sur carte | Je veux bloquer ma carte | API simulée | Action sensible |
| Commande de chéquier | Je veux demander un chéquier | API simulée | Demande bancaire |
| Demande de document | Je veux demander un relevé de compte | API simulée | Demande bancaire |
| Simulation crédit | Simule un crédit de 20 000 DT sur 5 ans | Module de calcul | Simulation |
| Message à l'agence | Rédige un message à mon agence | Template + saisie utilisateur | Assistance |
| Message au support | Je veux signaler un problème de connexion | Template + saisie utilisateur | Assistance |

### 7.2 Fonctionnalités hors MVP

Les fonctionnalités suivantes sont intéressantes mais ne seront pas prioritaires dans une première version :

- virement de masse ;
- virement permanent ;
- modèles de virement ;
- lettres de crédit ;
- transferts internationaux ;
- fichiers CFONB ;
- promotion immobilière ;
- gestion complète de la messagerie ;
- intégration réelle avec AMENet ;
- signature ou validation forte réelle.

## 8. Périmètre fonctionnel final retenu

Après analyse des fonctionnalités disponibles dans la démo AMENet, le périmètre du prototype est organisé autour de quatre blocs.

### 8.1 Consultation bancaire

Ce bloc concerne les fonctionnalités permettant au client de consulter des informations liées à ses comptes :

- vue d'ensemble des comptes ;
- consultation du solde ;
- recherche de mouvements ;
- affichage des dernières transactions ;
- historique des virements ;
- consultation des dépenses et revenus.

Ces fonctionnalités seront simulées à partir d'une base de données fictive.

### 8.2 Actions bancaires simulées

Ce bloc concerne les opérations que le chatbot peut préparer, mais jamais exécuter réellement :

- virement compte à compte ;
- virement vers bénéficiaire ;
- recharge de carte prépayée ;
- opposition sur carte ;
- commande de chéquier ;
- demande de carte ;
- demande de document.

Pour ces opérations, le chatbot devra toujours demander une confirmation explicite avant d'enregistrer la demande dans l'environnement de simulation.

### 8.3 Assistance et messagerie

Ce bloc concerne l'aide à la communication avec la banque :

- rédaction d'un message à l'agence ;
- rédaction d'un message au support ;
- préparation d'une demande structurée ;
- reformulation du problème rencontré par le client.

Le chatbot pourra aider l'utilisateur à rédiger un message clair, mais l'envoi réel sera simulé.

### 8.4 Simulation et aide à la décision

Ce bloc concerne les fonctionnalités de calcul ou d'analyse :

- simulation de crédit ;
- estimation de mensualité ;
- calcul de capacité d'emprunt ;
- résumé des dépenses ;
- analyse budgétaire simple.

Ces fonctionnalités seront développées sous forme de modules de calcul ou d'analyse à partir de données fictives.

## 9. Objets métier identifiés

L'analyse des interfaces permet d'identifier les principaux objets métier nécessaires à la simulation.

| Objet métier | Description | Utilisation dans le prototype |
|---|---|---|
| Client | Représente l'utilisateur connecté | Session fictive et personnalisation |
| Compte | Compte bancaire du client | Solde, virements, transactions |
| Transaction | Mouvement bancaire débit ou crédit | Historique, recherche, analyse budget |
| Carte | Carte bancaire ou prépayée | Opposition, recharge, déblocage international |
| Bénéficiaire | Personne ou compte destinataire d'un virement | Virement vers bénéficiaire |
| Virement | Ordre de transfert d'argent | Préparation et confirmation |
| Demande bancaire | Demande de document, carte, chéquier ou crédit | Suivi des demandes |
| Crédit | Simulation ou demande de financement | Calcul de mensualité et capacité d'emprunt |
| Message | Message à l'agence ou au support | Assistance et communication |
| Catégorie budget | Catégorie de dépense ou revenu | Analyse des dépenses |

## 10. Parcours conversationnels envisagés

### 10.1 Consultation du solde

Utilisateur : Quel est le solde de mon compte courant ?  
Chatbot : Votre compte courant se terminant par 3456 présente un solde disponible de 3 250,750 DT.

### 10.2 Recherche de mouvements

Utilisateur : Affiche mes opérations entre le 1er mai et le 12 mai.  
Chatbot : J'ai trouvé 4 opérations sur cette période. Le total des débits est de 430,000 DT et le total des crédits est de 1 200,000 DT.

### 10.3 Virement vers bénéficiaire

Utilisateur : Prépare un virement de 500 DT à mon fournisseur.  
Chatbot : D'accord. Pour préparer le virement, j'ai besoin du compte à débiter, du bénéficiaire, du montant, du motif et de la date d'exécution.  
Utilisateur : Depuis mon compte courant, bénéficiaire Société ABC, motif facture mai.  
Chatbot : Vous souhaitez effectuer un virement de 500 DT depuis votre compte courant vers Société ABC pour le motif « facture mai ». Confirmez-vous cette opération ?  
Utilisateur : Oui.  
Chatbot : Le virement a été enregistré dans l'environnement de simulation.

### 10.4 Opposition sur carte

Utilisateur : Je veux bloquer ma carte.  
Chatbot : Vous souhaitez faire opposition sur votre carte. Pour des raisons de sécurité, je vais afficher uniquement les cartes masquées. Quelle carte souhaitez-vous bloquer ?  
Utilisateur : Celle qui se termine par 4582.  
Chatbot : Confirmez-vous l'opposition sur la carte se terminant par 4582 ?  
Utilisateur : Oui.  
Chatbot : Votre demande d'opposition a été enregistrée dans l'environnement de simulation.

### 10.5 Recharge de carte prépayée

Utilisateur : Recharge ma carte prépayée de 100 DT.  
Chatbot : La recharge d'une carte prépayée doit respecter les règles observées dans la démo : le montant doit être un multiple de 10 DT et ne pas dépasser 500 DT. Confirmez-vous la recharge de 100 DT ?  
Utilisateur : Oui.  
Chatbot : La demande de recharge a été enregistrée dans l'environnement de simulation.

### 10.6 Demande de document

Utilisateur : Je veux demander un relevé de compte.  
Chatbot : Pour quel compte souhaitez-vous demander le relevé ?  
Utilisateur : Mon compte courant.  
Chatbot : Votre demande de document pour le compte courant a été enregistrée dans l'environnement de simulation.

### 10.7 Commande de chéquier

Utilisateur : Je veux commander un chéquier.  
Chatbot : D'accord. Pour quel compte souhaitez-vous demander un chéquier ?  
Utilisateur : Mon compte courant.  
Chatbot : Confirmez-vous la demande de chéquier pour votre compte courant ?  
Utilisateur : Oui.  
Chatbot : Votre demande de chéquier a été enregistrée dans l'environnement de simulation.

### 10.8 Simulation de crédit

Utilisateur : Simule un crédit de 20 000 DT sur 5 ans avec un revenu mensuel brut de 2 000 DT.  
Chatbot : D'après les informations saisies, la mensualité estimée est de X DT. Cette estimation est fournie à titre indicatif dans l'environnement de simulation.

### 10.9 Message au support

Utilisateur : Je n'arrive pas à me connecter à AMENet.  
Chatbot : Je peux vous aider à rédiger un message au support. Pouvez-vous préciser le navigateur utilisé et le message d'erreur affiché ?  
Utilisateur : J'utilise Chrome et la page reste bloquée.  
Chatbot : Voici un message proposé : « Bonjour, je rencontre un problème de connexion à AMENet. J'utilise le navigateur Chrome et la page reste bloquée au chargement. Merci de bien vouloir m'assister. »

## 11. Décisions de conception issues de l'analyse

### 11.1 Séparation entre information et action

Le chatbot doit distinguer les demandes informationnelles des demandes d'action. Une question comme « Comment faire opposition à ma carte ? » peut être traitée comme une réponse d'assistance. En revanche, une demande comme « Bloque ma carte » doit déclencher un parcours d'action avec confirmation explicite.

### 11.2 Utilisation de données simulées

Les données client, les comptes, les cartes, les transactions et les demandes seront simulés. Cela permet de développer le prototype sans manipuler de données sensibles.

### 11.3 Confirmation des opérations sensibles

Les actions comme le virement, l'opposition carte ou la recharge de carte prépayée ne doivent jamais être exécutées directement après une seule phrase utilisateur. Le chatbot doit reformuler l'action et demander confirmation.

Exemple :

Utilisateur : Je veux bloquer ma carte.  
Chatbot : Vous souhaitez faire opposition sur la carte se terminant par 4582. Confirmez-vous cette opération ?  
Utilisateur : Oui.  
Chatbot : Votre demande d'opposition a été enregistrée dans l'environnement de simulation.

### 11.4 Utilisation du RAG

Le RAG sera utilisé pour les questions générales sur les services bancaires et l'utilisation d'AMENet. Il ne sera pas utilisé pour les données personnelles du client. Les données personnelles simulées seront récupérées depuis une API ou une base structurée.

### 11.5 Orientation client professionnel

La présence de modules comme TPE, CFONB, virement de masse, bancaire étranger et lettres de crédit montre que l'interface AMENet observée cible fortement les clients professionnels ou entreprises. Le chatbot devra donc pouvoir répondre à des demandes de type professionnel, tout en gardant un premier périmètre simple.

### 11.6 Gestion des limites de la démo

Certaines pages de la démo n'affichent pas de formulaire complet, notamment les nouvelles demandes de chéquier, de carte et de document. Dans le prototype, ces fonctionnalités seront donc simulées à partir d'un modèle minimal : type de demande, compte concerné, date de création et statut de la demande.

## 12. Hypothèses de simulation

En l'absence d'accès aux données réelles, les hypothèses suivantes sont retenues :

- les clients utilisés sont fictifs ;
- les comptes, cartes et transactions sont simulés ;
- les opérations bancaires ne sont jamais réellement exécutées ;
- les actions sensibles nécessitent une confirmation explicite ;
- les données personnelles ne sont pas stockées dans la base vectorielle du RAG ;
- les questions générales peuvent s'appuyer sur une base documentaire ;
- les données personnelles simulées sont récupérées depuis des fichiers JSON ou une base locale ;
- l'envoi de messages à l'agence ou au support est simulé ;
- les demandes de chéquier, de carte et de document sont enregistrées comme demandes fictives.

## 13. Limites

Cette analyse se base uniquement sur les éléments visibles dans la démo AMENet et sur les informations publiques disponibles. Elle ne reflète pas nécessairement l'architecture interne réelle d'AMEN BANK.

Le prototype aura donc pour objectif de démontrer une architecture fonctionnelle, sécurisée et extensible, sans prétendre reproduire intégralement les systèmes bancaires existants.

Les principales limites identifiées sont :

- absence d'accès aux données réelles ;
- absence d'accès aux API internes ;
- absence d'intégration directe avec AMENet ;
- formulaires incomplets ou non visibles dans certaines pages de la démo ;
- impossibilité d'exécuter réellement des opérations bancaires ;
- nécessité de simuler les parcours sensibles ;
- nécessité de valider tout usage éventuel d'un modèle externe avec la banque.

## 14. Captures d'écran collectées

Les captures d'écran de la démo AMENet sont stockées dans le dossier suivant :

```text
data/raw/amenet_observations/
```
| Fichier                                   | Description                                       |
| ----------------------------------------- | ------------------------------------------------- |
| 01_vue_ensemble_comptes.png               | Vue d'ensemble des comptes et soldes              |
| 02_recherche_mouvements.png               | Formulaire de recherche de mouvements             |
| 03_mouvements_par_operation.png           | Consultation des mouvements par opération         |
| 04_cfonb_par_compte_periode.png           | Consultation CFONB par compte et par période      |
| 05_historique_cfonb_compte.png            | Historique CFONB par compte                       |
| 06_telechargement_documents.png           | Module de téléchargement de documents             |
| 07_virement_compte_a_compte.png           | Formulaire de virement compte à compte            |
| 08_consultation_mouvements_tpe.png        | Consultation des mouvements TPE                   |
| 09_recharge_carte_prepayee.png            | Recharge de carte prépayée                        |
| 10_deblocage_carte_internationale.png     | Déblocage carte internationale                    |
| 11_opposition_carte.png                   | Opposition sur carte                              |
| 12_bancaire_etranger_lettre_credit.png    | Lettre de crédit dans le module bancaire étranger |
| 13_services_fiche_promoteur.png           | Fiche promoteur dans le module services           |
| 14_financement_demande_credit.png         | Liste des demandes de crédit                      |
| 15_simulation_credit.png                  | Formulaire de simulation de crédit                |
| 16_change_bourse_cours_sicav.png          | Cours SICAV dans le module change/bourse          |
| 17_gestion_budget_parametrage.png         | Paramétrage de la période d'analyse budgétaire    |
| 18_messagerie_boite_reception.png         | Boîte de réception de la messagerie               |
| 19_services_demande_chequier.png          | Liste des demandes de chéquier                    |
| 20_services_demande_carte.png             | Liste des demandes de carte                       |
| 21_services_demande_document.png          | Liste des demandes de document                    |
| 22_virement_vers_beneficiaire.png         | Formulaire de virement vers bénéficiaire          |
| 23_virement_permanent_compte_a_compte.png | Formulaire de virement permanent compte à compte  |
| 24_messagerie_message_agence.png          | Formulaire de message à l'agence                  |
| 25_messagerie_message_support.png         | Formulaire de message au support                  |
| 26_gestion_budget_depenses_revenus.png    | Module dépenses et revenus                        |
| 27_gestion_budget_etat_depenses.png       | État des dépenses                                 |


## 15. Conclusion de l'analyse

L'analyse de la démo AMENet permet d'identifier un ensemble riche de fonctionnalités bancaires pouvant être adaptées à un chatbot assistant bancaire. Les fonctionnalités les plus pertinentes pour une première version sont celles qui combinent utilité utilisateur, simplicité de simulation et intérêt démonstratif : consultation du solde, recherche de mouvements, virement simulé, opposition carte, commande de chéquier, demande de document, simulation de crédit et assistance via messagerie.

Le prototype devra être conçu comme un système hybride combinant un module conversationnel, des données fictives structurées, des API simulées, un module de recherche documentaire pour les questions générales et des mécanismes de confirmation pour les opérations sensibles. Cette approche permet de construire une solution réaliste et extensible, tout en respectant les contraintes liées à l'absence d'accès aux systèmes bancaires réels.

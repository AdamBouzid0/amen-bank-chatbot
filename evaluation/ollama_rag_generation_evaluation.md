# Résultats de l'évaluation Ollama RAG generation

| metric                        |    value |
|:------------------------------|---------:|
| Nombre de questions           |    6     |
| Réponses Ollama acceptées     |    6     |
| Réponses fallback             |    0     |
| Taux acceptation Ollama       |    1     |
| Latence moyenne retrieval ms  |  303.8   |
| Latence moyenne génération ms | 6256.37  |
| Score top-1 moyen             |    0.869 |

## Détail par question

| question                                       | top1_title                                  |   top1_score | accepted_by_guardrail   | final_answer_source   |   retrieval_ms |   generation_ms |
|:-----------------------------------------------|:--------------------------------------------|-------------:|:------------------------|:----------------------|---------------:|----------------:|
| Comment faire opposition à une carte ?         | 10.4 Opposition sur carte                   |        0.879 | True                    | ollama                |         663.99 |         9694.64 |
| Quelles actions nécessitent une confirmation ? | 11.1 Séparation entre information et action |        0.858 | True                    | ollama                |         424.25 |         6328.93 |
| Comment commander un chéquier ?                | 10.7 Commande de chéquier                   |        0.851 | True                    | ollama                |         338.93 |         5115.05 |
| Comment demander un relevé de compte ?         | 10.6 Demande de document                    |        0.887 | True                    | ollama                |         191.39 |         5292.67 |
| Comment faire un virement ?                    | 10.3 Virement vers bénéficiaire             |        0.869 | True                    | ollama                |         158.9  |         5921.54 |
| Quels services sont disponibles sur AMENet ?   | 2. Périmètre de l'observation               |        0.872 | True                    | ollama                |          45.33 |         5185.4  |

## Exemple détaillé

**Question :** Comment faire opposition à une carte ?

**Brouillon sûr :**

Pour faire opposition à une carte dans le prototype, le chatbot identifie d'abord la carte concernée sans afficher de numéro complet. Il affiche uniquement des cartes masquées, par exemple avec les derniers chiffres visibles. Une fois la carte choisie, il demande une confirmation explicite avant d'enregistrer la demande d'opposition dans l'environnement de simulation. Aucune opération bancaire réelle n'est exécutée.

**Réponse finale :**

Pour faire opposition à une carte dans ce prototype, le chatbot identifie d'abord la carte concernée sans afficher son numéro complet. Il montre uniquement des cartes masquées, par exemple avec les derniers chiffres visibles. Une fois que vous avez choisi votre carte, il demande une confirmation explicite avant de l'enregistrer dans l'environnement de simulation pour simuler la demande d'opposition. Aucune opération bancaire réelle n'est effectuée.

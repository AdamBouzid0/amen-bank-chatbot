# Résultats de l'évaluation RAG retrieval

| metric                            |    value |
|:----------------------------------|---------:|
| Nombre de questions               |    8     |
| Questions avec retrieval cohérent |    8     |
| Taux de réussite top-k            |    1     |
| Latence moyenne retrieval ms      | 1594.41  |
| Score top-1 moyen                 |    0.869 |

## Détail par question

| question                                       | top1_title                                  |   top1_score |   keyword_hits_topk | retrieval_ok   |
|:-----------------------------------------------|:--------------------------------------------|-------------:|--------------------:|:---------------|
| Comment faire opposition à une carte ?         | 10.4 Opposition sur carte                   |        0.879 |                   3 | True           |
| Quelles actions nécessitent une confirmation ? | 11.1 Séparation entre information et action |        0.858 |                   3 | True           |
| Comment commander un chéquier ?                | 10.7 Commande de chéquier                   |        0.851 |                   3 | True           |
| Comment demander un relevé de compte ?         | 10.6 Demande de document                    |        0.887 |                   4 | True           |
| Comment faire un virement ?                    | 10.3 Virement vers bénéficiaire             |        0.869 |                   5 | True           |
| Quels services sont disponibles sur AMENet ?   | 2. Périmètre de l'observation               |        0.872 |                   2 | True           |
| Comment consulter mes mouvements bancaires ?   | 8.1 Consultation bancaire                   |        0.853 |                   4 | True           |
| Comment contacter le support AMENet ?          | 10.9 Message au support                     |        0.885 |                   2 | True           |
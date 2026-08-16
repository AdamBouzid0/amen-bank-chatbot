# Résultats de l'évaluation end-to-end du chatbot

| metric             |    value |
|:-------------------|---------:|
| Nombre d'étapes    |    10    |
| Étapes réussies    |    10    |
| Taux de réussite   |     1    |
| Latence moyenne ms |  1018.95 |
| Latence max ms     | 10148.9  |

## Détail du scénario

| name                         | category        | actual_intent    | actual_requires_confirmation   |   sources_count |   latency_ms | ok   |
|:-----------------------------|:----------------|:-----------------|:-------------------------------|----------------:|-------------:|:-----|
| Healthcheck backend          | health          | nan              |                                |               0 |        10.19 | True |
| Consultation solde           | consultation    | get_balance      | False                          |               0 |         6.34 | True |
| Consultation opérations      | consultation    | get_transactions | False                          |               0 |         3.67 | True |
| Préparation virement         | action_sensible | prepare_transfer | True                           |               0 |         3.78 | True |
| Confirmation virement        | confirmation    | confirm_action   | False                          |               0 |         5.46 | True |
| Préparation opposition carte | action_sensible | block_card       | True                           |               0 |         2.87 | True |
| Annulation opposition carte  | confirmation    | cancel_action    | False                          |               0 |         2.24 | True |
| Question documentaire RAG    | rag             | general_question | False                          |               3 |     10148.9  | True |
| Question hors périmètre      | hors_perimetre  | out_of_scope     | False                          |               0 |         3.84 | True |
| Demande sensible interdite   | securite        | out_of_scope     | False                          |               0 |         2.16 | True |
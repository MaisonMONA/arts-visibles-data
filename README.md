# MONA + Arts visibles : requêtes et données

Ce dépôt contient les requêtes SPARQL et les résultats associés pour le WikiProjet arts visibles par la maison MONA.

Résultats au format SPARQL 1.1 Query Results JSON Format : https://www.w3.org/TR/sparql11-results-json/

## Structure

Les requêtes sont classées dans le dossier `data/`.

Hiérarchie :

- Premier niveau : le nom de dossier indique le type d’entité principalement traité dans le dossier
- Second niveau : le nom de dossier indique les contraintes appliquées sur le type d’entité
- Le troisième niveau contient les fichiers :
  - query.rq : la requête
  - results.csv : résultats sous forme tabulaire
  - results.json : résultats au format SPARQL 1.1 Query Results JSON
  - values.rq (facultatif) : liste de valeurs sous forme de fragment SPARQL pouvant être injecté dans d’autres requêtes à des fins d’optimisaiton

Les requêtes peuvent être exécutées grâce au script `query.sh` en adaptant la variable `QUERY_FILE`, puis :

```bash
$ ./query.sh
```

## Recommandations

Coloration syntaxique SPARQL + CSV :

- Voir `.vscode/extensions.json`

Les résultats des requêtes qui commencent par cette ligne

```
#defaultView:Map
```

peuvent être visualisés sur la carte interactive du WDQS.

## Remarques techniques

- à discuter :
  - les fichiers de résultats ne sont pas commités pour l’instant, car ils vont créer d’énormes diff; les requêtes peuvent être exécutées avec `./query.sh`
  - partager une archive avec système de d’association requête → résultats
- `SERVICE wikibase:label` ralentit substantiellement le calcul; la plupart du temps, il vaut mieux passer directement par `rdfs:label`; attention au fallback
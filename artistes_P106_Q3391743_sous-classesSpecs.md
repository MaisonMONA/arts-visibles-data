# Reqûetes sur les artistes

Propriétés / valeurs pour identifier des artistes du Québec sur Wikidata 





## Identification du métier 

P106 occupation: artiste visuel·le Q3391743 & ses sous-classes 

*NB: à priori, on ne travaillera pas sur le domaine d'activité car ce serait trop chaotique*

Liste de modifications élaborée à partir de la requête: https://w.wiki/Td9E (209 résultats)

###  À retirer des résultats

retirer tout ce qui est une sous-classe de **cinéma (Q590870)**: film director, film editor, film maker, scenographer, cinematographer, documentary filmmaker, animator, stunt double, production manager
Liste des autres sous-classes à retirer:

```sparql
Q157798 # watchmaker
Q2079935 # architectural drafter
Q18545066 # stand-up comedian
Q22812942 # model railroader
Q957729 # photojournalist
Q1734662 # cartographer

```



### autres occupations P106 à ajouter 

```sparql
Q10988986 #arts textiles
Q2561815 #Bioart
```



## Identification du lieu 

wd:Q176 # Province du Québec et ce qui se trouve à l’intérieur

*penser à confirmer avec les résultats que les réserves (lieux de naissance de plusieurs artistes autochtones) sont considérées comme « à l’intérêt du Québec » dans l’ontologie de Wikidata*

### Lieu de travail P937

lieu d'exercice de l'activité professionnelle

### Résidence P551

Propriété notamment utilisée dans le projet de versement d’estampes de la BAnQ 



### Lieu de naissance P19 ?

tester la requête pour voir les résultats et décider si on veut inclure cette propriété : renseignée par le MAC et parfois par le MNBAQ aussi

Besoin de voir les résultats pour décider si on garde la propriété (probable)
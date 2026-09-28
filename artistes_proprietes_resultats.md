# Propriétés à afficher pour les artistes

→ fr si disponible, ensuite en, sinon ce qui existe :) 

QID, libellé, description

Trois requêtes avec les mêmes champs pour récupérer séparément 551, 937, 569

```sparql

# base
wdt:P106	#	occupation 
wdt:P551	#	lieu de résidence
wdt:P937	#	lieu de travail
wdt:P19	  #	lieu de naissance (ATTENTION : pas date de naissance)

# artistique et profession
wdt:P136	#	genre artistique genre_artistique
wdt:P101	#	domaine d'activité domaine_activite
wdt:P742	#	pseudonyme
wdt:P7763	#	statut des droits d'auteur du créateur ou de la créatrice 
wdt:P856	#	site officiel
wdt:P1875	#	représenté par 
wdt:P463	#	membre de
wdt:P1344	#	participant à
wdt:P166	#	distinction reçue
wdt:P6379	#	collection possédant une œuvre de la personne
wdt:P485	#	archives conservées par
wdt:P9493	#	dossier d'artiste détenu par
wdt:P767	#	collaborateur au travail de création

# identité
wdt:P21	  #	sexe ou genre
wdt:P569	#	date de naissance
wdt:P172	#	groupe ethnique
wdt:P1412	#	langue parlée, écrite ou signée

# meta
wdt:P1343	#	décrit par la source
wdt:P18   # image
```

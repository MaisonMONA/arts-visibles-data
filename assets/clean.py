from collections import Counter
from datetime import datetime
import json
import os


# source files
# adjuster le chemin si on exécute pas le script depuis la racine du répo
sources = [ 'assets/institutions_2026-10-06.json', 
            'assets/artistes_2026-09-26.json']
loaded_data = []

for src in sources:
    with open(src, "r", encoding='utf8') as fh:
        content = json.load(fh)
    loaded_data.append(content)

data_artistes = loaded_data[1]

# restructuration des données de Institutions
# 1. on a besoin que d'une sous section des données
data_institutions = loaded_data[0]['results']['bindings']
# 2. certaines valeurs doivent être "unpacked"
for n, entry in enumerate(data_institutions):
    for prop, value in entry.items():
        if isinstance(value, dict):
            #print(value['value'])
            data_institutions[n][prop] = value['value']
# à ce stade, les deux JSON sont une liste de résultats et chaque propriété a pour valeur une chaîne de caractères
print("- [x] Charger les fichiers JSON")


# Premier nettoyage : retirer les virgules et transformers les contenus multiples en listes
# TODO: garder pour Observable le fait de remplacer les cellules vides par null
def remove_commas(entries:list) -> list:
    for n, entry in enumerate(entries):
        for prop, value in entry.items():
            if isinstance(value, str):
                # transforme chaque entrée de propriété entre une liste d'éléments
                chunks = [chunk for chunk in value.split(",") if chunk != "," and len(chunk) > 0]
                entries[n][prop] = chunks
            else:
                print("!! erreur de formatage?")
                pass # ça ne devrait plus arriver
    return entries

data_artistes = remove_commas(data_artistes)
print("- [x] Retirer les virgules qui traînent dans les données artistes")

data_institutions = remove_commas(data_institutions) 
print("- [x] Retirer les virgules qui traînent dans les données institutions")


## Ajout d'une propriété "generation" pour les artistes
def assign_generation(birthdate:str) -> str:
    """étant donné une date (de naissance) au format YYYY-MM-DDTHH:MM:SSZ, renvoie le nom d'une génération"""
    def qdate(yyyy, mm=12, dd=31): 
        # quick datetime.date() creation
        return datetime(yyyy, mm, dd).date()

    # les dates générationnelles sont définies selon https://www12.statcan.gc.ca/census-recensement/2021/as-sa/98-200-X/2021003/98-200-X2021003-fra.cfm
    if not birthdate:
        return None
    else:
        yyyymmdd = birthdate.split("T")[0]
        parsed_date = datetime.strptime(yyyymmdd, "%Y-%m-%d").date()

        if parsed_date < qdate(1799):
            return "XVII-XVIIIe siècle"
        elif parsed_date < qdate(1899):
            return "XIXe siècle"
        elif parsed_date < qdate(1945):
            return "1900-1945"
        elif parsed_date < qdate(1965):
            return "1946-1965" # baby-boomers
        elif parsed_date < qdate(1980):
            return "1966-1980" # gen X
        elif parsed_date < qdate(1996):
            return "1981-1996" # gen Y
        elif parsed_date < qdate(2012):
            return "1997-2012" # gen Z
        elif parsed_date < qdate(2021):
            return "2013-2021" # gen Alpha (peu probable dans le dataset)
        else:
            return "problème de catégorisation"


for artiste in data_artistes:
    generation = None # réinitialisation à chaque itération
    # d'abord, s'il y a plusieurs dates, on arbitre en ne prenant que la première
    # les dates en double sont des intervals pour les incertitudes
    birthdate = artiste.get("date_naissance", [])

    # cas particulier
    if "http://www.wikidata.org/.well-known/genid/6d69ba6f759dbc8d7061878ae89c0f2f" in birthdate:  
        birthdate = []

    if len(birthdate) == 0:
        generation = "non renseigné"
    else:
        birthdate = birthdate[0]
        generation = assign_generation(birthdate)

    artiste['generation'] = [generation]


print("- [x] Ajouter une propriété 'generation' à chaque artiste")
print("\tINFO:", Counter(entry['generation'][0] for entry in data_artistes).most_common(10))


## Ajout d'une propriété "genre" pour les artistes
for n, artiste in enumerate(data_artistes):
    genre = None
    sexe_genre = artiste.get("sexe_genre", None)
    if not sexe_genre:
        genre = "non renseigné"
    elif "sexe ou genre non divulgué" in sexe_genre:
        genre = "non renseigné" 
    elif not set(sexe_genre).isdisjoint({"non-binarité", "transmasculinité", "femme trans", "homme trans", "transféminine", "genderqueer"}):
        genre = "transidentités"
    elif not set(sexe_genre).isdisjoint({"féminin", "femme cisgenre"}):
        genre = "féminin"
    elif not set(sexe_genre).isdisjoint({"masculin"}):
        genre = "masculin"
    else:
        genre = "nouveau cas à investiguer"
    
    data_artistes[n]["genre"] = [genre]

print("- [x] Ajouter une propriété 'genre' à chaque artiste")
print("\tINFO:", Counter(entry['genre'][0] for entry in data_artistes).most_common(10))


## Ajout d'une propriété "date_fondation" pour les institutions
for n, institution in enumerate(data_institutions):
    yyyymmdd = "" # pour être sûr que la valeur soit réinitialisée
    fondation = institution.get("fondation", [])
    if len(fondation) == 0:
        institution["date_fondation"] = None
    else:
        yyyymmdd = fondation[0].split("T")[0] # on ne garde que la première date s'il y en a plus d'une
        institution["date_fondation"] = [datetime.strptime(yyyymmdd, "%Y-%m-%d").year]
print("- [x] Ajouter une propriété 'date_fondation' à chaque institution")


## Ajout d'une propriété "catégorie_régionale" et d'une propriété "localisation_propre"

# # 1st combien d'entrée pour lieu vs. siege vs. localisation_administrative?
# loc_admins = [entry.get("localisation_administrative", ["no key"]) for entry in data_institutions]
# sieges = [entry.get("siege", ["no key"]) for entry in data_institutions]
# lieux = [entry.get("lieu", ["no key"]) for entry in data_institutions]
# print(len([l_a for l_a in loc_admins if len(l_a) == 0])) # = 0
# print(len([s for s in sieges if len(s) == 0])) # = 333
# print(len([l for l in lieux if len(l) == 0])) #  ) 277
# # Donc, je retiens la propriété localisation_administrative.

def clean_loc_admin(vals):
    # après vérification des entrées, nettoyage des valeurs pour conserver seulement la ville (pas le quartier, par la région administrative, pas la province...)
    if len(vals) <= 1:
        return vals
    elif vals == ['Chicoutimi', 'Saguenay']:
        return ['Saguenay']
    elif vals == ['Gallichan', 'Abitibi-Témiscamingue']:
        return ['Gallichan']
    elif vals == ['Montréal', 'Ahuntsic-Cartierville'] or vals == ['Montréal', 'Mercier–Hochelaga-Maisonneuve'] or vals == ['Québec', 'Montréal']:
        return ['Montréal']
    elif vals == ['Québec', 'Rimouski']:
        return ['Rimouski']
    elif vals == ['Québec', 'Rouyn-Noranda', 'Abitibi-Témiscamingue'] or vals == ['Rouyn-Noranda', 'Abitibi-Témiscamingue']:
        return ['Rouyn-Noranda']
    else:
        print("Pas de scénario prévu pour", vals)
        return vals


for institution in data_institutions:
    locad = clean_loc_admin(institution.get("localisation_administrative"))
    # on fait un nettoyage manuel pour ces données doubles ou triples
    ## if len(loc) > 1:
    ##     print(loc)
    ##     print(institution.get("institution"))
    # par contre, peut-on faire confiance à la valeur "Québec"? -> on va croiser avec la valeur lieu
    # dans les valeurs de "localisation_administrative" il y a des problèmes comme "village gai", "Université Concordia"

    
    # nettoyage manuel et semi-automatisée par comparaison avec val de lieu, qui n'est pas toujours aidante
    lieu = institution.get("lieu")

    if locad == ['Village gai']: # 2 cas: Q3558992 et Q124615636
        locad = ["Montréal"]
    elif locad == ['Université Concordia']: # 1 cas: Q5519005
        locad = ["Montréal"]
    elif locad == ['Mercier–Hochelaga-Maisonneuve']: # 1 cas: Q123921872
        locad = ["Montréal"]
    elif locad == ['Lachine']: # 1 cas: Q3329726
        locad = ["Montréal"]
    elif locad == ['Côte-des-Neiges–Notre-Dame-de-Grâce']: # 1 cas: Q104904446
        locad == ["Montréal"]

    elif locad == ['Québec'] and lieu:
        if lieu == ["Québec"] or lieu == ["plaines d'Abraham"] or lieu == ["Vieux-Québec"]:
            pass # alors la valeur reste inchangée
        elif lieu == ["Montréal"]:
            locad = ["Montréal"] # On corrige la valeur avant le calcul de cat_region
        elif "Montréal" in lieu:
            # on a 3 cas: 
            # ['Montréal', 'Toronto'] et 2 * ['Montréal', 'Québec']
            locad = ["Montréal"] # on prend la 1ere valeur de lieu
    elif locad == ['La Cité-Limoilou']: #
        locad =  ["Québec"] # 5 cas: Q1705530 ; Q130740932 ; Q2338135 ; Q28131538 ; Q62076089
    

    if not locad:
        institution["catégorie_régionale"] = ["non renseigné"]
    elif locad[0] == "Montréal":
        institution["catégorie_régionale"] = ["Montréal"]
    elif locad[0] == "Québec":
        institution["catégorie_régionale"] = ["ville de Québec"]
    else:
        institution["catégorie_régionale"] = ["Hors Montréal et ville de Québec"]
    institution["localisation_propre"] = locad # gardé pour pouvoir le proposer en visualisation, pour transparence

print("- [x] Ajouter une propriété 'catégorie_régionale' à chaque institution")
print("\tINFO:", Counter(entry['catégorie_régionale'][0] for entry in data_institutions).most_common(50))
print("- [x] Ajouter une propriété 'localisation_propre' à chaque institution")
#print("\tINFO:", Counter(entry['localisation_propre'] for entry in data_institutions).most_common(50))



new_file_artistes = "assets/artistes_propre.json"
new_file_institutions = "assets/institutions_propre.json"

with open(new_file_artistes, "w", encoding="utf8") as fh:
    fh.write(json.dumps(data_artistes, indent=2))

with open(new_file_institutions, "w", encoding="utf8") as fh:
    fh.write(json.dumps(data_institutions, indent=2))

print("- [x] Exporter les données dans de nouveaux fichiers JSON")
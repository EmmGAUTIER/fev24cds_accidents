#!/usr/bin/python3

import os
import sys
import pandas as pd
from premier_rapport import premier_rapport

rep_src = "données_origine/"
rep_dst = "données_travail/"

dful = []
dfll = []
dfvl = []
dfcl = []

dfrs = {}

fichiers_annuels = {
    "caracteristiques": {
        "rubrique": dfcl,
        "fichiers": [
            {"nom": "caracteristiques_2005.csv", "sep": ","},
            {"nom": "caracteristiques_2006.csv", "sep": ","},
            {"nom": "caracteristiques_2007.csv", "sep": ","},
            {"nom": "caracteristiques_2008.csv", "sep": ","},
            {"nom": "caracteristiques_2009.csv", "sep": "\t"},
            {"nom": "caracteristiques_2010.csv", "sep": ","},
            {"nom": "caracteristiques_2011.csv", "sep": ","},
            {"nom": "caracteristiques_2012.csv", "sep": ","},
            {"nom": "caracteristiques_2013.csv", "sep": ","},
            {"nom": "caracteristiques_2014.csv", "sep": ","},
            {"nom": "caracteristiques_2015.csv", "sep": ","},
            {"nom": "caracteristiques_2016.csv", "sep": ","},
            {"nom": "caracteristiques-2017.csv", "sep": ","},
            {"nom": "caracteristiques-2018.csv", "sep": ","},
            {"nom": "caracteristiques-2019.csv", "sep": ";"},
            {"nom": "caracteristiques-2020.csv", "sep": ";"},
            {"nom": "carcteristiques-2021.csv", "sep": ";"},
            {"nom": "carcteristiques-2022.csv", "sep": ";",
             "rename_cols": {"Accident_Id": "Num_Acc"}}
        ],
        "dtypes": {
            "Num_Acc": "object",
            "an": "int64",
            "mois": "int64",
            "jour": "int64",
            "hrmn": "object",
            "lum": "object",
            "agg": "int64",
            "int": "object",
            "atm": "object",
            "col": "object",
            "com": "object",
            "adr": "object",
            "gps": "object",
            "lat": "object",
            "long": "object",
            "dep": "object",
            "Accident_Id": "object"
        },
    },

    "usagers": {
        "rubrique": dful,
        "fichiers": [
            {"nom": "usagers_2005.csv", "sep": ","},
            {"nom": "usagers_2006.csv", "sep": ","},
            {"nom": "usagers_2007.csv", "sep": ","},
            {"nom": "usagers_2008.csv", "sep": ","},
            {"nom": "usagers_2009.csv", "sep": ","},
            {"nom": "usagers_2010.csv", "sep": ","},
            {"nom": "usagers_2011.csv", "sep": ","},
            {"nom": "usagers_2012.csv", "sep": ","},
            {"nom": "usagers_2013.csv", "sep": ","},
            {"nom": "usagers_2014.csv", "sep": ","},
            {"nom": "usagers_2015.csv", "sep": ","},
            {"nom": "usagers_2016.csv", "sep": ","},
            {"nom": "usagers-2017.csv", "sep": ","},
            {"nom": "usagers-2018.csv", "sep": ","},
            {"nom": "usagers-2019.csv", "sep": ";"},
            {"nom": "usagers-2020.csv", "sep": ";"},
            {"nom": "usagers-2021.csv", "sep": ";"},
            {"nom": "usagers-2022.csv", "sep": ";"}
        ],
        "dtypes": {
            "Num_Acc": "int64",
            "place": "object",
            "catu": "object",
            "grav": "object",
            "sexe": "object",
            "trajet": "object",
            "secu": "object",
            "locp": "object",
            "actp": "object",
            "etatp": "object",
            "an_nais": "object",
            "num_veh": "object",
            "id_vehicule": "object",
            "secu1": "object",
            "secu2": "object",
            "secu3": "object",
            "id_usager": "object"
        },
    },

    "vehicules": {
        "rubrique": dfvl,
        "fichiers": [
            {"nom": "vehicules_2005.csv", "sep": ","},
            {"nom": "vehicules_2006.csv", "sep": ","},
            {"nom": "vehicules_2007.csv", "sep": ","},
            {"nom": "vehicules_2008.csv", "sep": ","},
            {"nom": "vehicules_2009.csv", "sep": ","},
            {"nom": "vehicules_2010.csv", "sep": ","},
            {"nom": "vehicules_2011.csv", "sep": ","},
            {"nom": "vehicules_2012.csv", "sep": ","},
            {"nom": "vehicules_2013.csv", "sep": ","},
            {"nom": "vehicules_2014.csv", "sep": ","},
            {"nom": "vehicules_2015.csv", "sep": ","},
            {"nom": "vehicules_2016.csv", "sep": ","},
            {"nom": "vehicules-2017.csv", "sep": ","},
            {"nom": "vehicules-2018.csv", "sep": ","},
            {"nom": "vehicules-2019.csv", "sep": ";"},
            {"nom": "vehicules-2020.csv", "sep": ";"},
            {"nom": "vehicules-2021.csv", "sep": ";"},
            {"nom": "vehicules-2022.csv", "sep": ";"}
        ],
        "dtypes": {
            "Num_Acc": "int64",
            "senc": "object",
            "catv": "int64",
            "occutc": "object",
            "obs": "object",
            "obsm": "object",
            "choc": "object",
            "manv": "object",
            "num_veh": "object",
            "id_vehicule": "object",
            "motor": "object",
        },
    },
    "lieux": {
        "rubrique": dfll,
        "fichiers": [
            {"nom": "lieux_2005.csv", "sep": ","},
            {"nom": "lieux_2006.csv", "sep": ","},
            {"nom": "lieux_2007.csv", "sep": ","},
            {"nom": "lieux_2008.csv", "sep": ","},
            {"nom": "lieux_2009.csv", "sep": ","},
            {"nom": "lieux_2010.csv", "sep": ","},
            {"nom": "lieux_2011.csv", "sep": ","},
            {"nom": "lieux_2012.csv", "sep": ","},
            {"nom": "lieux_2013.csv", "sep": ","},
            {"nom": "lieux_2014.csv", "sep": ","},
            {"nom": "lieux_2015.csv", "sep": ","},
            {"nom": "lieux_2016.csv", "sep": ","},
            {"nom": "lieux-2017.csv", "sep": ","},
            {"nom": "lieux-2018.csv", "sep": ","},
            {"nom": "lieux-2019.csv", "sep": ";"},
            {"nom": "lieux-2020.csv", "sep": ";"},
            {"nom": "lieux-2021.csv", "sep": ";"},
            {"nom": "lieux-2022.csv", "sep": ";"}
        ],
        "dtypes": {
            "Num_Acc": "int64",
            "catr": "object",
            "voie": "object",
            "v1": "object",
            "v2": "object",
            "circ": "object",
            "nbv": "object",
            "pr": "object",
            "pr1": "object",
            "vosp": "object",
            "prof": "object",
            "plan": "object",
            "lartpc": "object",
            "larrout": "object",
            "surf": "object",
            "infra": "object",
            "situ": "object",
            "env1": "object",
            "vma": "float64",
        }
    }
}

for key, value in fichiers_annuels.items():  # Pour chaque rubrique
    nb_obs = 0  # nombre total d'observation (lignes, hors entêtes)

    print("Rubrique : ", key)
    dfl = value["rubrique"]
    dtype = value.get("dtypes")
    # print ("======>", dtype)

    for fichier_origine in value["fichiers"]:  # Pour chaque fichier annuel
        nom_fichier = fichier_origine["nom"]
        # lecture du fichier
        df = pd.read_csv(rep_src + nom_fichier,

                         sep=fichier_origine["sep"],
                         dtype=dtype,
                         encoding="latin_1",
                         index_col=False,
                         quotechar="\"",
                         low_memory=False)
        nb_obs += df.shape[0]
        if fichier_origine.get("rename_cols") is not None:
            df = df.rename(columns=fichier_origine.get("rename_cols"))
            print("-->  rename ", fichier_origine.get("rename_cols"))
        print(nom_fichier, df.shape)  # Pour info et mise au point
        # print(df.columns)
        # print(df.dtypes)
        dfl.append(df)

    dfrs[key] = pd.concat(dfl)  # Concaténation de tous les DataFrames annuels
    print("Nombre de DataFrames  : ", len(dfl))
    print("Nombre d'observations : ", nb_obs)

##############################################################################
# Enregistrement des 4 DataFrames et réalisation des rapports préliminaires
##############################################################################

phase = "_1"
for key, value in dfrs.items():  # Pour chaque rubrique (fichier csv)

    print("Rubrique : ", key)
    print("Taille : ", value.shape) # Pour contrôle

    nom_fichier_rub = rep_dst + key + phase +".csv"  # Nom du fichier rubrique multiannuel
    nom_fichier_desc = rep_dst + key +".json"  # Nom du fichier json de description
    nom_fichier_rapport = rep_dst + key + phase + ".txt"  # Nom du fichier description txt de rapport

    # Enregistrement du DataFrame rubrique
    print("Écriture de ", nom_fichier_rub)
    value.to_csv(nom_fichier_rub, sep='\t', index=False)

    # Élaboration du rapport
    print("Élaboration du rapport : ", nom_fichier_rapport)
    fichier_rapport = open(nom_fichier_rapport, "w")
    premier_rapport(nom_fichier_rub, sep='\t', max_list_len=30, csv_desc_name=nom_fichier_desc, outfile=fichier_rapport)
    fichier_rapport.close()

##############################################################################
# Modifications des données
##############################################################################

dfc = dfrs["caracteristiques"]
dfl = dfrs["lieux"]
dfu = dfrs["usagers"]
dfv = dfrs["vehicules"]

exit(0)

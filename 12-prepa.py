#!/usr/bin/python3

import sys
import pandas as pd
import re
import matplotlib.pyplot as plt
from premier_rapport import premier_rapport

# rep_src = "données_origine/"
rep_dst = "données_travail/"

# dfrs = {"caracteristiques":None, "lieux":None, "usagers":None, "vehicules":None}

phase_1 = "_1"
nom_fic_caractéristiques = rep_dst + "caracteristiques" + phase_1 + ".csv"
nom_fic_lieux = rep_dst + "lieux" + phase_1 + ".csv"
nom_fic_usagers = rep_dst + "usagers" + phase_1 + ".csv"
nom_fic_vehicules = rep_dst + "vehicules" + phase_1 + ".csv"

##############################################################################
# Préparation du fichiers des véhicules
##############################################################################
print()
print("----- Traitement : " + nom_fic_vehicules + " -----")
print()
print("  - Lecture")
dfv = pd.read_csv(nom_fic_vehicules,
                  sep='\t',
                  low_memory=False,
                  dtype={"Num_Acc": "object"})
print("  - Taille : ", dfv.shape)

# Sens de circulation
print("  - senc : sens de la circulation : remplacement NA en -1, conversion en int64")
dfv.senc = dfv.senc.fillna(-1)
dfv.senc = dfv.senc.astype("int64")

colonnes = ["senc", "catv","occutc", "obs","obsm", "choc","manv", "motor"]
print("  - ", colonnes, " : remplacement NA en -1, conversion en int64")
dfv[colonnes] = dfv[colonnes].fillna(-1)
dfv[colonnes] = dfv[colonnes].astype("int64")

colonnes = ["senc", "id_vehicule"]
print ("  - Suppression des colonnes : ", colonnes)
dfv = dfv.drop(colonnes, axis = 1)

print("  - Enregistrement")
dfv.to_csv("données_travail/vehicules_2.csv", sep='\t', index=False)
print("  - Réalisation du deuxième premier_rapport")
fichier_rapport = open(rep_dst + "vehicules_2.txt", "w")
premier_rapport(rep_dst + "vehicules" + "_2.csv",
                sep='\t',
                max_list_len=30,
                csv_desc_name=rep_dst + "vehicules" + ".json",
                outfile=fichier_rapport)
fichier_rapport.close()



##############################################################################
# Préparation du fichiers des usagers
##############################################################################

print("----- Traitement : " + nom_fic_usagers + " -----")
print("  - Lecture")
dfu = pd.read_csv(nom_fic_usagers,
                  sep='\t',
                  low_memory=False,
                  dtype={"Num_Acc": "object"})
print("  - Taille : ", dfu.shape)

print("  - place : remplacement des NA par -1")
dfu.place = dfu.place.fillna(-1)

print("  - trajet : remplacement des NA par -1")
dfu.trajet = dfu.trajet.fillna(-1)

print("  - locp : remplacement des NA par -1")
dfu.locp = dfu.locp.fillna(-1)

print("  - actp : remplacement des NA par -1")
dfu.actp = dfu.actp.fillna(-1)

print("  - etatp : remplacement des NA par -1")
dfu.etatp = dfu.etatp.fillna(-1)

# secu, secu1, secu2, secu3 conversion en entier
print("  - secu, secu1,2,3 : remplacement NA en -1, conversion en int64")
dfu.secu = dfu.secu.fillna(-1)
dfu.secu1 = dfu.secu1.fillna(-1)
dfu.secu2 = dfu.secu2.fillna(-1)
dfu.secu3 = dfu.secu3.fillna(-1)
dfu.secu = dfu.secu.astype("int64")
dfu.secu1 = dfu.secu1.astype("int64")
dfu.secu2 = dfu.secu2.astype("int64")
dfu.secu3 = dfu.secu3.astype("int64")

# Année de naissance, conversion en entier
print("  - an_nais :  remplacement NA en -1, conversion en int64")
dfu.an_nais = dfu.an_nais.fillna(-1)
dfu.an_nais = dfu.an_nais.astype("int64")

print("  - Enregistrement")
dfu.to_csv("données_travail/usagers_2.csv", sep='\t', index=False)
print("  - Réalisation du deuxième premier_rapport")
fichier_rapport = open(rep_dst + "usagers_2.txt", "w")
premier_rapport(rep_dst + "usagers" + "_2.csv",
                sep='\t',
                max_list_len=30,
                csv_desc_name=rep_dst + "usagers" + ".json",
                outfile=fichier_rapport)
fichier_rapport.close()

##############################################################################
# Préparation du fichiers des lieux
##############################################################################

print("----- Traitement : " + nom_fic_lieux + " -----")
print("  - Lecture")
dfl = pd.read_csv(nom_fic_lieux,
                  sep='\t',
                  low_memory=False,
                  dtype={"Num_Acc": "object", "catr": "float64"}  # ,
                  # na_values={"circ": ["-1", " -1"],
                  #           "nbv": ["-1", " -1"],
                  #           "prof": ["-1", " -1"],
                  #           "vosp": ["-1", " -1"],
                  #           "plan": ["-1", " -1"],
                  #           "larrout" : ["-1", " -1"],
                  #           "surf" : ["-1", " -1"],
                  #           "infra": ["-1", " -1"],
                  #           "situ": ["-1", " -1"],
                  #           }
                  )
print("  - Taille : ", dfl.shape)
# print (dfl.head(20))

# catr : Traitement des null et conversion en entiers
print("  - catr : Catégorie de route : remplacement null par -1, conversion en int")
dfl.catr = dfl.catr.fillna("-1")
# nbna = dfl.catr.isna().sum()
# print (" --> info() : ", dfl.info())
# print (" --> describe() : ", dfl.describe())
# dfl.catr = dfl.catr.astype('float64')
dfl.catr = dfl.catr.astype('int32')

# Traitement du régime de circulation
print("  - circ : Régime de circulation, remplacement des nulls et zéros par -1, conversion en int")
dfl.circ = dfl.circ.fillna("-1")
dfl.circ = dfl.circ.replace(0, -1)
dfl.circ = dfl.circ.astype("int64")

# nbv : Nombre de voies, des valeurs aberrantes, des nuls, ...
print("  - nbv : Nombre de voies, ")
dfl.nbv = dfl.nbv.replace(" -1", "-1")
dfl.nbv = dfl.nbv.replace("#ERREUR", "-1")
dfl.nbv = dfl.nbv.fillna("-1")
dfl.nbv = dfl.nbv.astype("int32")

# vosp : Voie spéciale, var catégorielle
print("  - vosp : Présence d'une voie réservée")
# dfl.vosp = dfl.vosp.replace(" -1", "-1")
dfl.vosp = dfl.vosp.fillna("-1")
dfl.vosp = dfl.vosp.astype("int32")

# prof : Déclivité
print("  - prof : Déclivité")
dfl.prof = dfl.prof.fillna("-1")
dfl.prof = dfl.prof.astype("int32")

# plan : Tracé en plan
print("  - plan : Tracé en plan")
dfl.plan = dfl.plan.fillna("-1")
dfl.plan = dfl.plan.astype("int32")

# État de la surface
print("  - surf : État de la surface")
dfl.surf = dfl.surf.fillna("-1")
dfl.surf = dfl.surf.astype("int32")

# Aménagement - infrastructure
print("  - infra : Aménagement - infrastructure; remplacement des null par -1 et conversion en int")
dfl.infra = dfl.infra.fillna("-1")
dfl.infra = dfl.infra.astype("int32")

# Aménagement - infrastructure
print("  - situ : Situation de l'accident; remplacement des null par -1 et conversion en int")
dfl.situ = dfl.situ.fillna("-1")
dfl.situ = dfl.situ.astype("int32")

# env1 ???
print("  - env1 : ? ? ? ; remplacement des null par -1 et conversion en int")
dfl.env1 = dfl.env1.fillna("-1")
dfl.env1 = dfl.env1.astype("int32")

# vma : Vitesse maximale autorisée
print("  - Vitesse maximale autorisée ; remplacement des null par -1 et conversion en int")
dfl.vma = dfl.vma.fillna("-1")
dfl.vma = dfl.vma.astype("int32")

print("  - Enregistrement : lieux_2.csv")
dfl.to_csv("données_travail/lieux_2.csv", sep='\t', index=False)
print("  - Réalisation du deuxième premier_rapport")
fichier_rapport = open(rep_dst + "lieux_2.txt", "w")
premier_rapport(dfl,
                sep='\t',
                max_list_len=30,
                csv_desc_name=rep_dst + "lieux" + ".json",
                outfile=fichier_rapport)
fichier_rapport.close()

##############################################################################
# Préparation du fichiers des caractéristiques
##############################################################################

print("----- Traitement : " + nom_fic_caractéristiques + " -----")
print("  - Lecture")
dfc = pd.read_csv(nom_fic_caractéristiques,
                  sep='\t',
                  low_memory=False,
                  dtype={"Num_Acc": "object"},
                  na_values={"lum": ["-1", " -1"],
                             "int": ["-1", " -1"],
                             "atm": ["-1", " -1"],
                             "col": ["-1", " -1"],
                             }
                  )
print("  - Taille : ", dfc.shape)

# Mise à 4 chiffres des années codées sur 2 chiffres
print("  - Mise à 4 chiffres de l'année (an)")
dfc.an = dfc.an.apply(lambda x: x if x > 2000 else x + 2000)

# Les département de métropole sont codés avec un 0 en ajouté, c. à d. multipliés par 10
# Les 10 premiers départements n'ont pas de zéro en tête contrairement à l'usage
#
print("  - Mise à 2 chiffres (métropole) ou 3 chiffres (DOM) des numéros de départements")
dfc.dep = dfc.dep.apply(lambda x: x if re.search("^97[123456]", x) != None else x[0:2])
dfc.dep = dfc.dep.apply(lambda x: x if re.search("^[1-9]$", x) == None else "0" + x)

# Inclusion du jour de la semaine
print("  - Inclusion du jour de la semaine dans le fichier")
df_date = dfc[["an", "mois", "jour"]]
df_date = df_date.rename({"an": "year", "mois": "month", "jour": "day"}, axis=1)
df_date["ts"] = pd.to_datetime(df_date)
df_date["jsem"] = df_date.ts.apply(lambda x: x.weekday())

dfc["jsem"] = df_date.jsem
df_date = None  # Libérons un peu de mémoire

print("  - Enregistrement")
dfc.to_csv("données_travail/caracteristiques_2.csv", sep='\t', index=False)
print("  - Réalisation du deuxième premier_rapport")
fichier_rapport = open(rep_dst + "caracteristiques_2.txt", "w")
premier_rapport(rep_dst + "caracteristiques" + "_2.csv",
                sep='\t',
                max_list_len=30,
                csv_desc_name=rep_dst + "caracteristiques" + ".json",
                outfile=fichier_rapport)
fichier_rapport.close()

exit(0)

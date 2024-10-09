#!/bin/sh
#
# Projet fev24cds_accidents
#
#  Emmanuel Gautier
#  Erika Méronville
#
#  Shell script pour télécharger les fichiers de données et documents
# des accidents de la circulation entre 2002 et 2022
#
# mawk est un dérivé de awk. Il lit la liste des fichiers avec,
# pour chaque fichier l'URL et le nom dans le répertoire courant.
# À exécuter dans le répertoire de destination (data/raw)

mawk -- '{system ("wget  " $2 " -O./données_origine/" $1) }' liste_telecharge.txt

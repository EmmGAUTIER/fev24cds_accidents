#!/bin/sh
#
# Affichage Pour chaque fichier de donnée :
#   - Son nom ; 
#   - Son nombre de lignes, y compris l'entête ;
#   - Les deux premières lignes (entête et première donnée)
#
# Ce script permet de vérifier le téléchargement et
# d'avoir une première idée du contenu. Il sert aussi
# à voir les séparateurs de colonnes (variables).
#
# usage : ./premier.sh |less
#
for f in ../data/raw/*csv
do
    echo
    echo $f  " :   " `cat $f | wc -l`
    head -n2 $f

done

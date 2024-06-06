#!/bin/bash
#./prep1.py
BASE=.
TABLES="caracteristiques lieux usagers vehicules"
REP_TRAVAIL=${BASE}/données_travail
REP_ORIGINE=${BASE}/données_origine

for tbl in $TABLES
do
    echo ""
    echo $tbl
    echo ""
    for f in  ${REP_ORIGINE}/*${tbl}*csv
    do
        #
        echo -n "$f   :  " ;head -n 2 $f # |sed 's/"//g'
    done
done
exit 0




#
cat données_travail/lieux.json | jq '.columns[] |  .name + ":" + .dtype '
#
#
#./regroupe.py

for tbl in $TABLES
do
    echo "--> " $tbl
    ./premier_rapport.py -s ',' --csv_desc ${tbl}.json  --max_list_len 30 ${REP_TRAVAIL}/${tbl}.csv 
done


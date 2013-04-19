#!/bin/bash

echo "date,heure,convocation,présent" > presents.csv;
cat extra_presences.csv >> presents.csv
for file in html/*; do
  out=$(echo $file | sed 's#^.*/##');
  python parse_PV.py $file json > json/$out;
  python parse_PV.py $file csv;
done >> presents.csv
#REFINE -> presents-refined.csv

awk -F ',' '{print $4}' presents-refined.csv |
 grep -v présent |
 sort |
 uniq > liste_elus.csv

awk -F "," '{print $1","$2}' presents-refined.csv |
 grep -v date |
 uniq |
 sed 's/-[0-9][0-9],.*$//' |
 sort |
 uniq -c |
 sed 's/^\s*//' |
 sed 's/ /,/' > total_reunions_mois.csv

awk -F ',' '{print $4}' presents-refined.csv |
 grep -v présent |
 sort |
 uniq -c |
 sed 's/^\s*//' | 
 sed 's/ /,/' > total_presences_elus.csv

awk -F ',' '{print $1","$2}' presents-refined.csv |
 grep -v date |
 sort |
 uniq -c |
 sed 's/^\s*//' |
 sed 's/ /,/' > total_presents_par_mois.csv

awk -F ',' '{print $4}' presents-refined.csv |
 grep -v présent |
 sort |
 uniq |
 while read line; do
  grep "$line" presents-refined.csv |
   awk -F ',' '{print $1,$4}' |
   sed 's/-[0-9][0-9] /,/' |
   sort |
   uniq -c |
   sed 's/^\s*//' |
   sed 's/ /,/' ;
 done > total_presences_elus_mois.csv


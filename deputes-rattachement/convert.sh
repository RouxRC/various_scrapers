#!/bin/bash

pdftohtml -xml Rattachement_partis_2014.pdf
./convert.py Rattachement_partis_2014.xml > rattachement-deputes-2014.csv

echo "## Rattachement financier des députés à un parti politique pour 2014" > README.md
echo >> README.md

echo "### Répartition des 577 députés par parti de rattachement :<br/>" >> README.md
cat rattachement-deputes-2014.csv |
 grep -v ',"rattachement_parti'   |
 awk -F '","' '{print $4}'        |
 sed 's/"$//'                     |
 sort | uniq -c >> README.md
echo >> README.md

echo "### Répartition des députés des différents groupe politique par parti de rattachement :<br/>" >> README.md
cat rattachement-deputes-2014.csv |
 grep -v ',"rattachement_parti'   |
 awk -F '","' '{print $3" - "$4}' |
 sed 's/"$//'                     |
 sort | uniq -c >> README.md
echo >> README.md

dat=$(date "+%d/%m/%Y")
echo "sources : [Assemblée nationale](http://www.assemblee-nationale.fr/qui/Rattachement_partis_2014.pdf) le $dat" >> README.md

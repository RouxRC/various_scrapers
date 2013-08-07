#!/bin/bash

# Conversion du pdf en xml indiquant les positions du texte
pdftohtml -xml reserve-2012.pdf # -> reserve-2012.xml

# Extraction du contenu des tableaux par identification visuelle à tâtons des zones à extraire
python convert_xml.py reserve-2012.xml > reserve-2012.csv

# Nettoyage de colonnes par clustering dans Open refine -> reserve-2012.refined.csv

# Ajout des urls NosDéputés/NosSénateurs et récup groupe parl
ct=0
mkdir -p cache
rm -f reserve-2012-extra-infos.csv
cat reserve-2012.refined.csv | while read line; do
  url=$(echo $line |
        grep ",\(Assemblée nationale\|Sénat\)$" |
        sed 's#^.*,\([^,]\+\),Assemblée nationale$#http://2007.nosdeputes.fr/\1/xml#' |
        sed 's#^.*,\([^,]\+\),Sénat$#http://nossenateurs.fr/\1/xml#' |
        sed 's#\(.*\) \(.*\)#\1%20\2#' |
        sed 's#\(.*\) \(.*\)#\1%20\2#' |
        sed 's#\(.*\) \(.*\)#\1%20\2#' |
        sed 's#\(.*\) \(.*\)#\1%20\2#')
  if ! test -z "$url"; then
    md5=$(echo "$url" | md5sum | sed 's/\s\+.*$//')
    if ! test -f "cache/$md5.cache"; then
      curl -sL "$url" |
        grep 'groupe_sigle>' |
        sed 's/<\/groupe_sigle>.*$//' |
        sed 's/^.*sigle>//' > "cache/$md5.cache"
    fi
    groupe=$(cat "cache/$md5.cache")
  else
    groupe=""
  fi
  echo "$ct : $groupe / $url"
  echo "$line,$groupe,$url" >> reserve-2012-extra-infos.csv
  ct=$(($ct + 1))
done

# Ajout des headers manquants et de la colonne "part prise en charge" avec LibreOffice


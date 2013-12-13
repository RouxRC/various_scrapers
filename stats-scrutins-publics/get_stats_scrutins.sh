#!/bin/bash

if [ ! -z "$1" ] || [ ! -s html/2013-2014.html ]; then
  mkdir -p html
  for y in 11 12 13; do
    z=$(($y + 1))
    curl -sL "http://www.assemblee-nationale.fr/14/scrutins/table-20$y-20$z.asp" |
     iconv -f "iso-8859-15" -t "utf-8" > html/20$y-20$z.html
  done
fi

cat html/20*.html         |
 tr "\n\r" " "            |
 sed 's/\s\+/ /g'         |
 sed 's#</#\n</#g'        |
 grep 'class="denom"'     |
 grep -v "N° de scrutin"  |
 sed 's/\s*<[^>]*>\s*//g' |
 sort > scrutins.txt

tot=$(cat scrutins.txt | wc -l)
sol=$(grep '\*' scrutins.txt | wc -l)
pub=$(($tot - $sol))
fl_s=$((100 * $sol / $tot))
fl_p=$((100 * $pub / $tot))
rat_s="$fl_s,"$((1000 * $sol / $tot - 10 * $fl_s))
rat_p="$fl_p,"$((1000 * $pub / $tot - 10 * $fl_p))
dat=$(date "+%d/%m/%Y")

echo "### Ratio de scrutins publics et solennels à l'Assemblée nationale

Depuis le début de la 14ème législature en juin 2012, $tot scrutins électroniques se sont déroulés.<br/>
Parmi eux, seuls $sol scrutins solennels (soit $rat_s%) mentionnent le nom de chacun des députés votants.<br/>
Les $pub autres scrutins ($rat_p%) dits « publics » ne mentionnent que la liste des rebelles de chaque groupe.<br/>
Pour en savoir plus, voir la [note de Regards Citoyens](http://www.regardscitoyens.org/documents/notes/20130110-RegardsCitoyens-AN-transparence-des-votes.pdf).

sources : [Assemblée nationale](http://www.assemblee-nationale.fr/14/scrutins/) le $dat" > README.md

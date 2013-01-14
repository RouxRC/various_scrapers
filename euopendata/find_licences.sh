#!/bin/bash

mkdir -p tmp
echo "dataset_url;licence_url;licence" > eulicences.csv

maxpage=`curl "http://open-data.europa.eu/open-data/data/dataset?page=1" | grep '"/open-data/data/dataset?page=..."' | sed 's#^.*/open-data/data/dataset?page=\([0-9]\{3\}\)#\1#' | sed 's/".*$//'`
for i in `seq $maxpage`; do
  echo "Process page $i"
  curl "http://open-data.europa.eu/open-data/data/dataset?page=$i" --connect-timeout 30 --retry 5 -s -S > tmp/recherche-$i.html
  if [ `grep -vc rights tmp/recherche-$i.html` -eq 0 ]; then
    curl "http://open-data.europa.eu/open-data/data/dataset?page=$i" --connect-timeout 30 --retry 5 -s -S > tmp/recherche-$i.html
  fi
  grep "/data/dataset/" tmp/recherche-$i.html | sed 's/^.* href="//' | sed 's/">.*$//' > tmp/recherche-$i.urls
  for u in `cat tmp/recherche-$i.urls`; do
    id=`echo $u | sed 's#^.*data/dataset/##'`
    url=`echo "http://open-data.europa.eu$u"`
    if ! test -e tmp/dataset-$id.html; then
      curl "$url" --connect-timeout 30 --retry 5 -s -S > tmp/dataset-$id.html
    fi
    if [ `grep -vc rights tmp/dataset-$id.html` -eq 0 ]; then
      curl "$url" --connect-timeout 30 --retry 5 -s -S > tmp/dataset-$id.html
    fi
    grep 'rel="dc:rights"' tmp/dataset-$id.html | sed 's#^.*href="#'"$url"';#' | sed 's/" rel="dc:rights">/;/' | sed 's#</a></span>.*$##' >> eulicences.csv
  done
  awk -F ";" '{print $3}' eulicences.csv | sort | uniq -c | sort
done


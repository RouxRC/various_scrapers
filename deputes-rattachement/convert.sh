#!/bin/bash

pdftohtml -xml Rattachement_partis_2014.pdf
./convert.py Rattachement_partis_2014.xml > rattachement-deputes-2014.csv


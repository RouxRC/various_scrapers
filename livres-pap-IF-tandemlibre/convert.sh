#!/bin/bash

pdftops 1990-2005.pdf - | psselect -p1-185 | ps2pdf14 - 1990-2005-clean.pdf
pdftohtml -xml 1990-2005-clean.pdf
python convert-1990.py 1990-2005-clean.xml > 1990-2005.csv

pdftops 2005-2007.pdf - | psselect -p5-48 | ps2pdf14 - 2005-2007-clean.pdf
pdftohtml -xml 2005-2007-clean.pdf
python convert-2005.py 2005-2007-clean.xml > 2005-2007.csv


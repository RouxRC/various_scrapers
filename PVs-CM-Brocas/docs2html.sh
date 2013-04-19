#!/bin/bash

# on enlève les espaces dans les noms !!!

rename 's/ /_/g' */* * */*/* */*/*/*
# on convertit en html
cd doc; for i in `find . -type d`; do echo $i; mkdir ../html/$i; cd $i; libreoffice --headless  --convert-to html *.doc*  ; cd - ;   done ; cd ..;
# on convertit en pdf
cd doc; for i in `find . -type d`; do echo $i; mkdir ../pdf/$i; cd $i; libreoffice --headless  --convert-to pdf *.doc*  ; cd - ;   done ; cd ..;

# on remet les html et pdf en place ! (l'option outdir de  libreoffice ne semble pas marcher) 

cd doc; for i in `find . -type d`; do echo $i; mv $i/*.pdf ../pdf/$i;  done ; cd ..;

cd doc; for i in `find . -type d`; do echo $i; mv $i/*.html ../html/$i;  done ; cd ..;

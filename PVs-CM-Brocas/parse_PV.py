#!/usr/bin/env python                                                                                                                                      
# -*- coding: utf-8 -*-

import re, sys, pprint

with open(sys.argv[1], 'r') as PV:
    text = PV.read()

data = {'date': '', 'heure': '', 'convocation': '', 'session' : '', 'president': '', 'presents': [], 'excuses': [], 'absents': [], 'secretaire': '', 'secretaire_adjoint': ''}

re_html = re.compile(r'<[^>]*>')
clean_html = lambda x: re_html.sub('', x)

text = text.replace('&#160;', ' ')
re_split_lines = re.compile(r'</p>')
text = re_split_lines.sub('\n</p>', text)

months={'janvier': '01', 'fevrier': '02', 'mars': '03', 'avril': '04', 'mai': '05', 'juin': '06', 'juillet': '07', 'aout': '08', 'septembre': '09', 'octobre': '10', 'novembre': '11', 'decembre': '12'}
def convert_month(text):
    month = text.lower().strip().replace('É', 'e').replace('é', 'e').replace('û', 'u').replace('Û', 'u')
    if month in months:
        return months[month]
    return text

re_split = re.compile(r"([ \-'])")
def lowerize(text):
    res = ""
    for a in re_split.split(text):
        if len(a) < 2:
            res += a
        else:
            res += a[0]+a[1:].lower().replace('É', 'é').replace('È', 'è').replace('À', 'à').replace('Î', 'î').replace('Ï', 'ï').replace('Ô', 'ô').replace('Ù', 'ù').replace('Û', 'û').replace('Ü', 'ü')
    return res.strip()

re_dash = re.compile(r' *(– *)+ *')
re_exceptions = re.compile(r' -[    ]+M')
re_clean_blanks = re.compile(r'[    \s]+')
def handle_elus(text, field):
    text = re_dash.sub('–', re_clean_blanks.sub(' ', re_exceptions.sub(' – M', text.strip(' –'))))
    res = []
    for elu in text.split('–'):
        nom = lowerize(elu)
        if nom not in data[field]:
            data[field].append(nom)

nohtml = clean_html(text)
re_assemble_lines = re.compile(r' *–[  \n]+M')
nohtml = re_assemble_lines.sub(' – M', nohtml)

#print nohtml
#print text

re_match_date = re.compile(r'(S(?:E|È|è)ANCE|PROC(?:E|È|è)S.*VERBAL|[cC]onvocation).*\D(\d+)[eErR]* *([\wéû]+) *(\d{4})')
re_match_time = re.compile(r"Le .* DU MOIS D(?:'|’|E ).* (?:à|A|À) *(\d+) *H\w* *(\d+)?", re.I)
re_match_session = re.compile(r'Le Conseil .* r(?:é|É|e)uni en session ([\w\-]+) .* pr(?:é|É|e)sidence de (.+).', re.I)
re_match_presents = re.compile(r' *PR(?:é|É|E|e)SENTS? *: *(.+)')
re_match_absents = re.compile(r'ABSEN[TC]E?S? (NON *)?EXCUS(?:é|É|E|e)E?S? *: *(.+)')
re_match_secretaire = re.compile(r'((auxiliaire).*)?Secr(?:é|É|e)taire(?: de s(?:é|É|e)ance)?(?: désignée)?( *\w+)? *: *(.+)', re.I)
re_match_secretaire2 = re.compile(r'(M\w+ .*) est désignée secr(?:é|É|e)taire', re.I)


for line in nohtml.split('\n'):
    line = line.strip()
    if not line:
        continue
    if len(sys.argv) > 3:
        print " - TESTLINE : %s" % line
    heures = re_match_time.search(line)
    if heures:
        mins = 0
        if heures.group(2):
            mins = int(heures.group(2))
        data['heure'] = "%02d:%02d" % (int(heures.group(1)), mins)
    dates = re_match_date.search(line)
    if dates:
        field = ""
        if "onvocati" in dates.group(1) and not data['convocation']:
            field = "convocation"
        elif not data['date']:
            field = "date"
        if field:
            data[field] = "%04d-%s-%02d" % (int(dates.group(4)), convert_month(dates.group(3)), int(dates.group(2)))
    seances = re_match_session.search(line)
    if seances:
        data['session'] = seances.group(1).strip(' –')
        data['president'] = lowerize(seances.group(2).strip(' –'))
    presents = re_match_presents.search(line)
    if presents:
        handle_elus(presents.group(1), 'presents')
    absents = re_match_absents.search(line)
    if absents:
        if absents.group(1):
            handle_elus(absents.group(2), 'absents')
        else:
            handle_elus(absents.group(2), 'excuses')
    secretaire = re_match_secretaire.search(line)
    if secretaire:
        option = ""
        if secretaire.group(1):
            option = "(%s) " % secretaire.group(2).strip(' –')
        if secretaire.group(3):
            option = "(%s) " % secretaire.group(3).strip(' –')
        if option:
            data['secretaire adjoint'] = secretaire.group(4).strip(' –')
        else:
            data['secretaire'] = secretaire.group(4).strip(' –')
    else:
        secretaire = re_match_secretaire2.search(line)
        if secretaire:
            data['secretaire'] = secretaire.group(1).strip(' –')

if (sys.argv[2] == "json"):
    pprint.pprint(data)
else:
    for a in data['presents']:
        print "%s,%s,%s,%s" % (data['date'],data['heure'],data['convocation'],a)

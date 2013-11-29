#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

filepath = sys.argv[1]
with open(filepath, 'r') as xml_file:
    xml = xml_file.read()

drawMap = False
if len(sys.argv) > 2:
    drawMap = True

topvals = []
leftvals = []
results = []
type_map = {'a': 'Arts',
            'a-l': 'Arts;Lettres',
            'j': 'Jeunesse',
            'l': 'Lettres',
            'p': 'Philosophie',
            's': 'Sciences',
            'sh': 'Sciences Sociales et Humaines',
            'p/ssh': 'Philosophie;Sciences Sociales et Humaines',
            'ssh': 'Sciences Sociales et Humaines',
            'ssh-p': 'Sciences Sociales et Humaines;Philosophie',
            'ssh-p-l': 'Sciences Sociales et Humaines;Philosophie;Lettres',
            'sshn': 'Sciences Sociales et Humaines',
            'shh': 'Sciences Sociales et Humaines',
            'st': 'Sciences et Techniques'}
headers = ['pays', 'nom pap', 'auteur', 'titre', 'editeur', 'type', 'editeur trad']
record = ["", "", "", "", "", "", ""]
oddpage = True
pap = False
read = True
lastleft = 0
country = ""
pap_name = ""
auteur = ""
lastauteur = ""
re_line = re.compile(r'<page number|text top="(\d+)" left="(\d+)"[^>]*font="(\d+)">(.*)</text>', re.I)
save = False
for line in (xml+('\n<text top="765" left="1" font="10">a</text>')).split("\n"):
    #print "DEBUG %s" % line
    if '<page number' in line:
        oddpage = not oddpage
        continue
    if not line.startswith('<text'):
        continue
    attrs = re_line.search(line)
    if not attrs or not attrs.groups():
        print "WARNING : line detected with good font but wrong format %s" % line
        continue
    top = int(attrs.group(1))
    if top < 26 or top > 765:
        continue
    topvals.append(top)
    left = int(attrs.group(2))
    if oddpage:
        left += 21
    leftvals.append(left)
    if drawMap:
        continue
    font = int(attrs.group(3))
    text = attrs.group(4).replace("&amp;", "&")
    #print "DEBUG %s %s %s %s" % (font, left, top, text)
    if save or left < lastleft - 300:
        #print "DEBUG GO %s" % record
        if not record[5]:
            if not results:
                continue
            lastrecord = results.pop()
            results.append(lastrecord)
        if record[5]:
            record[0] = country
            record[1] = pap_name
            record[2] = auteur.replace(' )', ')').replace(' ,', ',')
            results.append(record)
            lastauteur = auteur
            auteur = ""
            record = ["", "", "", "", "", "", ""]
        save = False
    if font == 0:
        if read:
            country = ""
            read = False
        if text.startswith("•"):
            pap = True
            pap_name = ""
            continue
        if not text.startswith("-"):
            text = " %s" % text
        if pap:
            pap_name += text
        else:
            country += text
    elif font == 1:
        if pap:
            if text == "AP":
                continue
            pap_name += text
        else:
            country += text
    elif font < 4 and left < 313:
        if pap:
            pap = False
            read = True
        if font == 2 and not text.startswith("-"):
            text = " %s" % text
        if 62 < left < 66:
            auteur = ""
        auteur += text
    elif "<i>" in text:
        if not auteur:
            auteur = lastauteur
        if left == 315:
            record[3] = ""
        record[3] += text.replace("<i>", "").replace("</i>", "") + " "
    elif "<b>" in text:
        if text.startswith("<b>"):
            record[5] = type_map[text.replace("<b>", "").replace("</b>", "").lower()]
        else:
            tmp = text.split("<b>")
            record[4] += tmp[0].strip() + " "
            record[5] = type_map[tmp[1].replace("<b>", "").replace("</b>", "").strip().lower()]
    elif font == 2 and left < 800:
        record[4] += text + " "
    elif font == 2:
        record[6] += text + " "
        save = True
    lastleft = left

if not drawMap:
    print ",".join(['"%s"' % h for h in headers])
    for i in results:
        for j in range(len(i)):
            i[j] = i[j].strip()
        print ",".join([str(i[a]) if isinstance(i[a], int) else "\"%s\"" % i[a].replace('"', '""') for a,_ in enumerate(i)])

else:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    filename = "1990-2005"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True, fillstyle='left')
    plt.xticks(np.arange(-150, 1450, 50))
    ax.plot(leftvals, topvals, 'ro', marker=".")
    fig.savefig("%s.png" % filename)
    fig.clf()
    plt.close(fig)


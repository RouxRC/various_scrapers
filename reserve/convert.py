#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

filepath = sys.argv[1]
with open(filepath, 'r') as xml_file:
    xml = xml_file.read()

topvals = []
leftvals = []
y = []
results = []
record = ["", "", "", 0, 0, "", ""]
lasttop = 0
re_line = re.compile(r'<text top="(\d+)" left="(\d+)"[^>]*>(.*)</text>', re.I)
for line in xml.split("\n"):
    #print "DEBUG %s" % line
    if 'font="0"' in line or 'font="1"' in line or 'font="2"' in line:
        attrs = re_line.search(line)
        if not attrs.groups():
            #print "WARNING : line detected with good font but wrong format %s" % line
            continue
        top  = int(attrs.group(1))
        topvals.append(top)
        left = int(attrs.group(2))
        leftvals.append(left)
        text = attrs.group(3)
        if "<b>" in line or "</b>" in line:
            #print "skip headers %s (%d/%d)" % (text, top, left)
            continue
        #print "DEBUG GO %s" % text.replace(' ', '').replace('€','')
        if abs(lasttop - top) > 40:
            if record[6]:
                for i in [0,1,2,5,6]:
                    record[i] = record[i].strip()
                try:
                    record[2] = record[2][0].upper()+record[2][1:].replace('&#34;', '"')
                except Exception as e:
                    print record
                    exit(1)
                results.append(record)
            record = ["", "", "", 0, 0, "", ""]
        if left < 200:
            record[0] += text
        elif 200 <= left < 330:
            record[1] += text.replace(' ', '').replace('20A', '2A').replace('20B', '2B')
        elif 330 <= left < 735:
            record[2] += text
        elif 735 <= left < 810:
            record[3] += int(text.replace(' ', '').replace('€',''))
        elif 810 <= left < 890:
            record[4] += int(text.replace(' ', '').replace('€',''))
        elif 890 <= left < 1050:
            record[5] += text
        elif 1050 <= left:
            record[6] += text
        lasttop = top

if record[6]:
    results.append(record)

print '"Bénéficiaire","Département","Nature du projet","Coût du projet (€)","Subvention allouée (€)","Dossier transmis par","Nature de la réserve"'
for i in results:
    print ",".join([str(i[a]) if isinstance(i[a], int) else "\"%s\"" % i[a].replace('"', '""') for a,_ in enumerate(i)])

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

filename = "test"
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True, fillstyle='left')
plt.xticks(np.arange(-150, 1450, 50))
ax.plot(leftvals, topvals, 'ro', marker=".")
fig.savefig("%s.png" % filename)
fig.clf()
plt.close(fig)


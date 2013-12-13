#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

filepath = sys.argv[1]
with open(filepath, 'r') as xml_file:
    xml = xml_file.read()

drawMap = False
if len(sys.argv) > 2:
    drawMap = True

page = 0
topvals = {}
leftvals = {}
maxtop = 0
results = []
headers = ['nom', 'prénom', 'groupe', 'rattachement_parti']
record = ["", "", "", ""]
re_line = re.compile(r'<page number|text top="(\d+)" left="(\d+)"[^>]*font="(\d+)">(.*)</text>', re.I)
save = False
for line in (xml).split("\n"):
    #print "DEBUG %s" % line
    if line.startswith('<page'):
        page += 1
    if not line.startswith('<text'):
        continue
    attrs = re_line.search(line)
    if not attrs or not attrs.groups():
        print "WARNING : line detected with good font but wrong format %s" % line
        continue
    font = int(attrs.group(3))
    top = int(attrs.group(1))
    if top > maxtop:
        maxtop = top
    if (page == 1 and top < 110) or (page == 11 and top > 950):
        continue
    if not font in topvals:
        topvals[font] = []
    topvals[font].append(top)
    left = int(attrs.group(2))
    if not font in leftvals:
        leftvals[font] = []
    leftvals[font].append(left)
    if drawMap:
        continue
    text = attrs.group(4).replace("&amp;", "&")
    #print "DEBUG %s %s %s %s" % (font, left, top, text)
    if left < 40:
        record[0] = text
    elif left < 240:
        record[1] = text
    elif left < 375:
        if "<b>" in text:
            a = text.split(' <b>')
            record[2] = a[0].replace('app.', '')
            record[3] = a[1]
        else:
            record[2] = text
    else:
        record[3] = text
    if record[3]:
        results.append(record)
        record = ["", "", "", ""]

if not drawMap:
    print ",".join(['"%s"' % h for h in headers])
    for i in results:
        for j in range(len(i)):
            i[j] = i[j].replace('<b>', '').replace('</b>', '').strip()
        print ",".join([str(i[a]) if isinstance(i[a], int) else "\"%s\"" % i[a].replace('"', '""') for a,_ in enumerate(i)])

else:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import cm

    fig = plt.figure(figsize=(8.5, 12))
    ax = fig.add_subplot(111)
    ax.grid(True, fillstyle='left')
    nf = len(leftvals)
    for font in leftvals:
        color = cm.jet(1.5*font/nf)
        ax.plot(leftvals[font], topvals[font], 'ro', color=color, marker=".")
        plt.figtext((font+1.)/(nf+1), 0.95, "font %d" % font, color=color)
    maxleft = (maxtop + 50) * 8.5 / 12
    plt.xticks(np.arange(0, maxleft, 50))
    plt.yticks(np.arange(0, maxtop + 50, 50))
    plt.xlim(0, maxleft)
    plt.ylim(0, maxtop + 50)
    plt.gca().invert_yaxis()
    fig.savefig("map.png")
    fig.clf()
    plt.close(fig)


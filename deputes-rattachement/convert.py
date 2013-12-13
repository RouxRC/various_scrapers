#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

filepath = sys.argv[1]
with open(filepath, 'r') as xml_file:
    xml = xml_file.read()

drawMap = False
if len(sys.argv) > 2:
    drawMap = True

topvals = {}
leftvals = {}
results = []
headers = ['nom', 'prénom', 'groupe', 'rattachement_parti']
record = ["", "", "", ""]
re_line = re.compile(r'<page number|text top="(\d+)" left="(\d+)"[^>]*font="(\d+)">(.*)</text>', re.I)
save = False
for line in (xml).split("\n"):
    #print "DEBUG %s" % line
    if not line.startswith('<text'):
        continue
    attrs = re_line.search(line)
    if not attrs or not attrs.groups():
        print "WARNING : line detected with good font but wrong format %s" % line
        continue
    font = int(attrs.group(3))
    top = int(attrs.group(1))
    #if top < 115 or top > 820:
    #    continue
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
    from matplotlib import cm

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True, fillstyle='left')
    plt.xticks(np.arange(-150, 1450, 50))
    for font in leftvals:
        ax.plot(leftvals[font], topvals[font], 'ro', color=cm.jet(1.*font/len(leftvals)), marker=".")
    fig.savefig("map.png")
    fig.clf()
    plt.close(fig)


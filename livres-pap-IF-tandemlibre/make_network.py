#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Library to write graph data into JSON or GEXF (Gephi Network files)
"""

import simplejson as json
import networkx as nx
from networkx.readwrite import json_graph

def write_graph_in_format(graph, filename, fileformat='gexf') :
    if fileformat.lower() == 'json':
        return json.dump(json_graph.node_link_data(graph), open(filename,'w'))
    return nx.write_gexf(graph, filename)

def add_node(graph, node, **args):
    if graph.has_node(node):
        graph.node[node]['total'] += 1
    else:
        graph.add_node(node, label=node, total=1, **args)

def add_edge(graph, node1, node2):
    if graph.has_edge(node1, node2):
        graph[node1][node2]['weight'] += 1
    else:
        graph.add_edge(node1, node2, weight=1)

with open('1990-2013.json') as f:
    data = json.loads(f.read())

G = nx.Graph()
for line in data['rows']:
    add_node(G, line['editeur'], type="editeur", pays="France")
    add_node(G, line['editeur trad'], type="editeur_trad", pays=line['pays'])
    add_edge(G, line['editeur'], line['editeur trad'])
write_graph_in_format(G, '1990-2013.gexf')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
import networkx as nx

edges = [[0, 1, 1],
         [0, 2, 3],
         [0, 3, 7],
         [1, 2, 1],
         [2, 3, 2]]
nodes = [0, 1, 2, 3]
g = nx.Graph()
g.add_nodes_from(nodes)
g.add_weighted_edges_from(edges)
length, path = nx.bidirectional_dijkstra(g, 0, 3)
print(length, path)
g.remove_node(0)
g.remove_edge(0, 1)

# -*- coding: utf-8 -*-
"""
@author Hamsavardhini
"""
import networkx as nx
import community
from py2neo import Graph as pGraph
from igraph import Graph as iGraph
import matplotlib.pyplot as plt
from matplotlib import pylab
from collections import Counter

def show_graph(partition):
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(neoGraph)
    count = 0.
    for com in set(partition.values()):
        count += 1
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        nx.draw_networkx_nodes(neoGraph, pos, list_nodes, node_size = 20,
                                    node_color = str(count / size))
    nx.draw_networkx_edges(neoGraph,pos, alpha=0.5)
    plt.show()

def detect_community(neoGraph):
    # partition graph for community detection
    parts = community.best_partition(neoGraph)
    # membership value of each node
    values = [parts.get(node) for node in neoGraph.nodes()]
    generate_graph(neoGraph,"graph_with_community.pdf",values)
    # print parts
    return parts

def generate_graph(graph,file_name,values):
    # initialze Figure
    plt.figure(num=None, figsize=(18, 18), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos,node_color=values)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.2
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name)
    pylab.close()
    del fig

def calucate_modularity(graph):
    partitions = detect_community(graph)
    print "Clustering modularity"
    print community.modularity(partitions,graph)

def find_giant(neoGraph):
    big_cluster_nodes = []
    partitions = detect_community(neoGraph)
    cluster_dict = Counter(v for v in partitions.values()) # dictionary with cluster id and node count
    big_cluster_count = max(cluster_dict.values())# large cluster's by node count
    big_cluster_id = cluster_dict.keys()[cluster_dict.values().index(big_cluster_count)]
    for k,v in partitions.items():
        if v == big_cluster_id:
            big_cluster_nodes.append(k)
    print '%s%d%s%d%s' % ("cluster id ", big_cluster_id, " is the biggest cluster with ", big_cluster_count, " nodes")
    print cluster_dict

if __name__ == "__main__":
    # Graph initialization
    neo4j = pGraph("http://localhost:7474/db/data/")
    query = "Match(n)-[r]-(c) return n,r,c"
    # Query the entire graph
    data = neo4j.cypher.execute(query)
    # py2noe to IGraph
    ig = iGraph.TupleList(data)
    ig.write_graphml(f="dheepan.graphml")
    # IGraph to networkx
    neoGraph = nx.read_graphml('dheepan.graphml')
    # print nx.info(neoGraph)
    detect_community(neoGraph)
    calucate_modularity(neoGraph)
    find_giant(neoGraph)


# -*- coding: utf-8 -*-
"""
@author Hamsavardhini
"""
from py2neo import Graph as pGraph
from igraph import Graph as iGraph
import re

neo4j = pGraph("http://localhost:7474/db/data/")
query = "Match(n)-[r]->(c) return n,c"
data = neo4j.cypher.execute(query)

ig = iGraph.TupleList(data)
new_dict = {}
attributes = []
clusterID = []

class clustering(object):
    def walktrap(self):
        wcluster = ig.community_walktrap().as_clustering()
        self.modularity = wcluster.modularity
        self.membership = wcluster.membership
        self.num_of_clusters = max(wcluster.membership) + 1
        # print self.num_of_clusters
        # print len(self.membership)
        # print self.modularity
        # ig.write_svg("walktrap.svg",layout=ig.layout_kamada_kawai())

    def match_input(self):
        self.walktrap()
        attrib, clustid = self.parse_node_values()
        clust_dict = dict(zip(attrib, clustid))
        for k, v in clust_dict.iteritems():
                new_dict.setdefault(v, []).append(k)
        return new_dict

    def parse_node_values(self):
        for item, cluster_id in zip(ig.vs["name"], self.membership):
            if str(item).find('uri') != -1:
                attribute = re.search('info:(.+?),uri', str(item)).group(1).replace('"', '')
                uri = re.search('resource(.+?)$', str(item)).group(1).replace('_', ' ').replace('"', '')
                attributes.append(uri) if attribute == uri else attributes.append(attribute)
                clusterID.append(cluster_id)
        return attributes, clusterID

c = clustering()
c.match_input()
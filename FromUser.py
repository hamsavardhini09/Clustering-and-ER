# -*- coding: utf-8 -*-
"""
@author Hamsavardhini
"""
from ClusterNeo4j import clustering as c
import itertools
import difflib
import sys

cluster_dict = {}
cluster_numbers = []
cluster_dict = c().match_input()
# new_cluster_dict = {}
profile = []
form = ''

class entity_resolution(object):

    def sim(self, fn1, fn2):
        return difflib.SequenceMatcher(None, fn1, fn2).ratio()

    def resolve_entities(self):
        counter = 1
        while counter <= 3:
            attribute = self.get_user_input()
            cluster_numbers = self.resolve_clusters(attribute, cluster_dict)
            print cluster_numbers
            if len(cluster_numbers) > 1:
                for a, b in itertools.combinations(cluster_numbers, 2):
                    score = self.sim(','.join(cluster_dict[a]), ','.join(cluster_dict[b]))
                    if score < 0.1:
                        print "less"
                        for cluster in a, b:
                            profile.append(cluster_dict[cluster])
                            form = 'Schrodinger'
                    else:
                        print "ok"
                        form = 'Definite' if len(cluster_numbers) == 1 else "Probabilistic form...with clusters %d", len(cluster_numbers)
                        for i in cluster_numbers:
                            profile.append(cluster_dict[i])
            else:
                for i in cluster_numbers:
                    profile.append(cluster_dict[i])
            counter += 1
        print profile

    def resolve_clusters(self, attribute, cluster_dict):
        for k, v in cluster_dict.iteritems():
            if set(attribute).issubset(set(v)):
                cluster_numbers.append(k)
                break
        return cluster_numbers

    def get_user_input(self):
        attribute = raw_input('Enter attribute(s) of an entity name seperated by commas: <enter *stop* if you dont have attribtues to resolve> ').split(',')
        return attribute if 'stop' not in attribute else sys.exit(1)

if __name__ == '__main__':
    er = entity_resolution()
    er.resolve_entities()
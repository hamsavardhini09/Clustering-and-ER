# -*- coding: utf-8 -*-
"""
@author Hamsavardhini
"""
from py2neo import Node, Relationship, authenticate, Graph as pGraph
import pandas
import os.path
# configuration file
import config

# set up authentication parameters
authenticate("localhost:7474", "neo4j", "neo4j")
# connect to authenticated graph database
graph = pGraph("http://localhost:7474/db/data/")
# clear the graph before start loading
graph.delete_all()

data = pandas.read_excel(os.path.join(config.results_dir, 'Output_Murphy Choy.xls'))

username = "Murphy Choy"

surfaceform, url, uri, relations = ([] for x in range(4))

for index, x in data.iterrows():
    # print x['surfaceform']
    surfaceform.append(x.values[1].encode('ascii', 'ignore'))
    url.append(x.values[3].encode('ascii', 'ignore'))
    uri.append(x.values[2].encode('ascii', 'ignore'))
    if str(x.values[0]) != "nan":
        exp = str(x.values[0]).replace(':', ',').split(',')
        relations.append(exp[(len(exp)-1)].encode('ascii', 'ignore'))
    else:
        relations.append('others')


def constraint(node_label, node_property):
    # graph = Graph("http://localhost:7474/db/data/")
    schema = graph.schema
    if node_property not in schema.get_uniqueness_constraints(node_label):
        schema.create_uniqueness_constraint(node_label, node_property)

# constraint("Person", "name")
constraint("Entity", "uri")
constraint("Link", "url")

# person = graph.merge_one("Person", "name", username)
# person = Node("Person", name=username)

for x, y, z, m in zip(relations, surfaceform, uri, url):
    exist_entity_node = graph.find_one("Entity", property_key="uri", property_value=z.lower())
    if exist_entity_node is None:
        i = graph.merge_one("Entity", "info", y.lower())
        i.properties.update({
            'uri': z.lower()})
        graph.push(i)
    else:
        i = graph.merge_one("Entity", "info", y.lower())

    j = graph.merge_one("Link", "url", m.lower())

    # graph.create_unique(Relationship(person, x.lower(), i))
    graph.create_unique(Relationship(i, "source", j))

# graph.delete_all()
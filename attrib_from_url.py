# -*- coding: utf-8 -*-
"""
@author Hamsavardhini
"""
from py2neo import Graph
from py2neo.server import GraphServer
import pandas as pd
import config
graph = Graph("http://localhost:7474/db/data/")
server = GraphServer(config.Neo4jHome)

def get_attributes(urlList):
    attributes_dict = {}
    print "setting....."
    print server.conf.set("neo4j-server","org.neo4j.server.database.location","neo4j.db")
    print server.conf.get("neo4j-server","org.neo4j.server.database.location")
    server.home
    for i in urlList:
        attribute = "match (url)<-[source_link]-(attributes) where url.url=\"" + i + "\" return attributes.propertyValue as value, attributes.uri as uri,attributes.propertyName as type"
        result = graph.cypher.execute(attribute)
        df = pd.DataFrame(result.records, columns=result.columns)
        attributes_dict[i] = df['value']
    print attributes_dict
    find_match(attributes_dict)

maxi = []
def find_match(dic):
    for k in dic:
        print k
        maxi = 0
        j=''
        for ambit in range(len(dic)-1):
            if k != dic.keys()[ambit]:
                length = return_matches(dic[k],dic.values()[ambit])
                if (length > maxi):
                    maxi = length
                    j = dic.keys()[ambit]
        print "for"
        print j, maxi

def return_matches(a, b):
    return len(list(set(a) & set(b)))
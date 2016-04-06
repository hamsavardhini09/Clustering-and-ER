# -*- coding: utf-8 -*-
"""
@author Hamsavardhini
"""

from py2neo import Graph
from attrib_from_url import get_attributes
import config
import os
from loadNeo4j import load_data

def remove_duplicates():
    remove_query = '''start r=relationship(*)
                   match (s)-[r]->(e)
                   with s,e,type(r) as typ, tail(collect(r)) as coll
                   foreach(x in coll | delete x)'''
    graph.cypher.execute(remove_query)

def retrieveURL():
    distinctSourceLinks = "match (n) where (Has(n.url)) return n"
    for urls in graph.cypher.execute(distinctSourceLinks):
        urlList.append(urls[0]['url'].encode('utf-8'))
    return urlList

def get_data_dirs():
    result_dir = config.result_dir
    data_dirs = []
    for subdir, dirs, files in os.walk(result_dir):
        data_dirs.append(subdir)
    return data_dirs[1:]

def clear_data():
    distinctSourceLinks = "match (n) where (Has(n.url)) return n"

if __name__ == "__main__":
    urlList = []
    #graph = Graph("http://localhost:7474/db/data/")
    graph = Graph("http://localhost:7474/db/data/")
    for data_dir in get_data_dirs():
        print "directory " + data_dir
        load_data(data_dir)
        print "load over"
        get_attributes(retrieveURL())
        print "clearing data"
        #clear_data()
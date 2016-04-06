from math import*

def jaccard_similarity(x,y):

 intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
 union_cardinality = len(set.union(*[set(x), set(y)]))
 print intersection_cardinality
 print union_cardinality
 return intersection_cardinality/float(union_cardinality)

print jaccard_similarity(["singapore","smu","chennai"],["singapore","text mining","yelp","ieee","trip advisor"])
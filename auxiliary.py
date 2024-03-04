import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import pickle
import time

G = nx.Graph()
G.add_edges_from([(1, 4), (4, 5), (1, 2), (2,3), (3,5), (3,6), (6,5), (2,4)])
source = 1
destination = 6

#pos = nx.spring_layout(G, k=0.65)  # Adjust k to increase spacing
#nx.draw(G, pos, with_labels=True)
#plt.show()
path_list = list(nx.edge_disjoint_paths(G,source,destination))
print(path_list)
#print(random.choice(3))

k= 3
n=10
g = nx.random_regular_graph(k,n)
#g =nx.read_gml("benchmark_graphs/BtEurope.gml") 
#pos = nx.spring_layout(g, k=0.65)  # Adjust k to increase spacing
#nx.draw(g, pos, with_labels=True)
#plt.show()
edge_list = list(g.edges())
print(edge_list)
liste= [1,4,6]
array = np.array([[1,4,7]])
print(liste)
print(array)
array2 = np.append(array,[liste], axis=0)
print(array2)
nodes = list(g.nodes())
print(nodes)
print(nodes)
print(nodes)

#source = random.choice(nodes)
#destination = random.choice(nodes)
#while destination == source:
#    destination = random.choice(nodes)

numbers = [1,2,3]
print(len(numbers))
result = zip(numbers, numbers[1:])
print(result)
print(list(result))

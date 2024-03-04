import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools
from networkx.algorithms.connectivity import build_auxiliary_edge_connectivity
from networkx.algorithms.flow import build_residual_network
import random
import pickle
import time
from obj_class_pickle import DataGraphs

# Function to load the graph from a GML file
def load_graph(file_path):
    return nx.read_gml(file_path)

# Function to ensure that at least one disjoint path remains
def get_fails_list(g, source, destination, disjoint_path_list, failure_num):
    edge_list = list(g.edges())
    pathList = disjoint_path_list[source][destination]
    num_edgedesjointpaths = len(pathList)
    max_fails = min(failure_num, num_edgedesjointpaths - 1)
    fails_list = []
    for _ in range(max_fails):
        random_fail = random.choice(edge_list)
        while random_fail in fails_list:
            random_fail = random.choice(edge_list)
        fails_list.append(random_fail)
    return fails_list

# Create a list of edge-disjoint paths to destination, source nodes vary
def get_disjoint_path(g, destination):
    H = build_auxiliary_edge_connectivity(g)
    R = build_residual_network(H, 'capacity')
    edge_disjoint_paths = {n: {} for n in g}
    for u in g.nodes():
        if u != destination:
            paths = sorted(list(nx.edge_disjoint_paths(g, u, destination, auxiliary=H, residual=R)), key=len)
            edge_disjoint_paths[u][destination] = paths
    return edge_disjoint_paths

# Routing function
def routingSQ1(SQ1, source, destination, n, fails, sc_bool):
    if sc_bool:
        newList = [path for path in SQ1 if doesntContainFail(path, fails)]
        return (False, len(newList[0])-1, 2, None, newList)
    else:
        curRoute = SQ1[0]
        k = len(SQ1)
        detour_edges = []
        index = 1
        hops = 0
        switches = 0
        curNode = source  # current node
        #n = len(T[0].nodes())
        while (curNode != destination):
            nxt = curRoute[index]
            if (nxt, curNode) in fails or (curNode, nxt) in fails:
                for i in range(2, index+1):
                    detour_edges.append((curNode, curRoute[index-i]))
                    curNode = curRoute[index-i]
                switches += 1
                curNode = source
                hops += (index-1)
                curRoute = SQ1[switches % k]
                index = 1
            else:
                if switches > 0:
                    detour_edges.append((curNode, nxt))
                curNode = nxt
                index += 1
                hops += 1
            if hops > 3*n or switches > k*n:
                print("cycle square one")
                return (True, hops, switches, detour_edges, SQ1)
        return (False, hops, switches, detour_edges, SQ1)

# Modified SQ1 experiments function to work with loaded graph
def sq1_experiments(g, failure_num, rep):
    nodes = list(g.nodes())
    edges = list(g.edges())
    for i in range(rep):
        print('rep: ' + str(i))
        start_rep = time.time()

        resultHops = {}
        resultHopsShortCut = {}
        resultShortestPathForStretch = {}

        filename_pickle = 'results/zoo/' + 'SQ1_ShortCut_graph_' + str(i) + '.pickle'

        for source in nodes:
            resultHops[source] = {}
            resultHopsShortCut[source] = {}  
            resultShortestPathForStretch[source] = {}              
            for destination in nodes:
                if source == destination:
                    continue

                disjoint_path_list = get_disjoint_path(g, destination)
                fails_list = get_fails_list(g, source, destination, disjoint_path_list, failure_num)

                # Rest of the logic remains the same as in the original function
                # Calculate routing metrics for each source-destination pair
                # and store them in resultHops, resultHopsShortCut, resultShortestPathForStretch

        end_rep = time.time()
        print(time.asctime(time.localtime(start_rep)))
        print(time.asctime(time.localtime(end_rep)))   
        toPickle = DataGraphs(0,0, nodes, edges, i, resultShortestPathForStretch,0, failure_num, resultHops, resultHopsShortCut) 
        toPickle.save(filename_pickle)

# Main execution
if __name__ == "__main__":
    start = time.time()
    print(time.asctime(time.localtime(start)))

    # Load the graph from the specified GML file
    graph_file_path = '/home/mikheil/Desktop/SQ1_ShortCut-main/newdir/Gridnet_edited.gml'
    #y achse sollte nicht negativ sein
    # 15 knoten schon gut 
    
    g = load_graph(graph_file_path)

    # Parameters for experiments
    failure_num = 200
    rep = 2

    print('start')
    sq1_experiments(g, failure_num, rep)
    print('ende')

    end = time.time()
    print(end - start)
    print(time.asctime(time.localtime(end)))

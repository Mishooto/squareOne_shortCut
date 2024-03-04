import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools
from networkx.algorithms.connectivity import build_auxiliary_edge_connectivity
from networkx.algorithms.flow import build_residual_network
import random
import json
import time

# Function to create graphs
def create_graphs(n, k, rep, seed):
    g = nx.random_regular_graph(k, n)
    while nx.edge_connectivity(g) < k:  # Ensure connectivity of k or greater
        g = nx.random_regular_graph(k, n).to_directed()
    g.graph['seed'] = seed
    g.graph['k'] = k
    return g

# Function to get disjoint paths
def get_disjoint_path(g, destination):
    SQ1 = {}
    H = build_auxiliary_edge_connectivity(g)
    R = build_residual_network(H, 'capacity')
    SQ1 = {n: {} for n in g}
    for u in g.nodes():
        if u != destination:
            paths = sorted(list(nx.edge_disjoint_paths(g, u, destination, auxiliary=H, residual=R)), key=len)
            SQ1[u][destination] = paths
    return SQ1

# Function to check for fails in edge-disjoint paths
def doesntContainFail(path, fails):
    zipped = list(zip(path, path[1:]))
    return all(fail not in zipped for fail in fails)

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
        curNode = source
        while curNode != destination:
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

# Function to create a list of fails, either random or specifically on edge-disjoint paths
def get_fails_list(g, source, destination, disjoint_path_list, fail_random, failure_num):
    edge_list = list(g.edges())
    pathList = disjoint_path_list[source][destination]
    fails_list = []
    if fail_random:
        for i in range(failure_num):
            random_fail = random.choice(edge_list)
            while random_fail in fails_list:
                random_fail = random.choice(edge_list)
            fails_list.append(random_fail)
    else:
        for path in pathList:
            nodeindex_in_path = random.randint(0, len(path)-2)
            fails_list.append((path[nodeindex_in_path], path[nodeindex_in_path+1]))
    return fails_list

# SQ1 experiments
def sq1_experiments(n, k, failure_num, rep, seed, ran_dom, fail_random):
    if ran_dom:        
        for i in range(rep):
            print('rep: '+ str(i))
            start_rep = time.time()
            g = create_graphs(n, k, i, seed)
            nodes = list(g.nodes())
            edges = list(g.edges())
            resultHops = {}
            resultHopsShortCut = {}
            resultShortestPathForStretch = {}
            filename_json = 'results/zoo2/' + 'SQ1_ShortCut_' + str(seed) + '_graph_' + str(ran_dom) + '_' + str(n) + '_' + str(len(edges)) + '_' + str(i) + '_' + str(fail_random) + '_' + str(failure_num) + '.json'
            for source in nodes:
                resultHops[source] = {}
                resultHopsShortCut[source] = {}
                resultShortestPathForStretch[source] = {}
                for destination in nodes:
                    if source == destination:
                        continue
                
                    disjoint_path_list = get_disjoint_path(g, destination)
                    fails_list = get_fails_list(g, source, destination, disjoint_path_list, fail_random, failure_num)

                    hop_list = []
                    hop_list_shortcut = []
                    for j in range(0, len(fails_list)):
                        fails_sublist = fails_list[:j]
                        [_, hops, _, _, _] = routingSQ1(disjoint_path_list[source][destination], source, destination, n, fails_sublist, sc_bool=False)
                        [_, hopsS, _, _, _] = routingSQ1(disjoint_path_list[source][destination], source, destination, n, fails_sublist, sc_bool=True)
                        hop_list.append(hops)
                        hop_list_shortcut.append(hopsS)
                    
                    resultHops[source][destination] = hop_list
                    resultHopsShortCut[source][destination] = hop_list_shortcut
                    resultShortestPathForStretch[source][destination] = len(disjoint_path_list[source][destination][0])-1

            # Save as JSON
            data_for_json = {
                "seed": seed,
                "random": ran_dom,
                "nodes": nodes,
                "edges": edges,
                "experiment_index": i,
                "resultShortestPathForStretch": resultShortestPathForStretch,
                "fail_random": fail_random,
                "failure_num": failure_num,
                "resultHops": resultHops,
                "resultHopsShortCut": resultHopsShortCut
            }
            with open(filename_json, 'w') as json_file:
                json.dump(data_for_json, json_file, indent=4)

            end_rep = time.time()
            print(time.asctime(time.localtime(start_rep)))
            print(time.asctime(time.localtime(end_rep)))
    else:
        g = nx.read_gml("benchmark_graphs/BtEurope.gml")

# Initialize parameters for experiments, take runtime, start experiments
if __name__ == "__main__":
    start = time.time()
    print(time.asctime(time.localtime(start)))
    seed = 1
    n = 20
    rep = 5
    k = 8
    failure_num = 18
    ran_dom = True
    fail_random = False
    print('start')
    sq1_experiments(n, k, failure_num, rep, seed, ran_dom, fail_random)
    print('ende')
    end = time.time()
    print('Total execution time:', end - start)
    print(time.asctime(time.localtime(end)))

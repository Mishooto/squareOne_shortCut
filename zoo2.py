import sys
import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools
from networkx.algorithms.connectivity import build_auxiliary_edge_connectivity
from networkx.algorithms.flow import build_residual_network
import random
import json
import time




#TODO: fehler draufschmeißen auf edge disjoint pfade bis der kurzeste weg getroffen wurde, wie viele alternative kantendisjunkte pfade hast du? solltest mindestes 1 haben,
#TODO: fehler passiert, wir brauchen mehr hops
#TODO: Y achse hops x achse number of fails, unda gavdes kibeebs für 1,2,3,4,5,6,7, failures im system da kibe aiweva 
#ausklamösern
#TODO: update ro gaaketos yovelif ehleris mere ro tavidan ipovos kurzeste pfad 
#erdos rini graph random graph network x idan
#kunstliche graphen machen mit verschiedenen knoten kantenmengen, 20 knoten 50 knoten 

# Function to load the graph from a GML file
def load_graph(file_path):
    return nx.read_gml(file_path)

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


# Function to ensure that at least one disjoint path remains
def get_fails_list(g, source, destination, disjoint_path_list, failure_num):
    edge_list = list(g.edges())
    pathList = disjoint_path_list[source][destination]
    num_edgedisjointpaths = len(pathList)
    max_fails = min(failure_num, num_edgedisjointpaths - 1)
    fails_list = []
    for _ in range(max_fails):
        #randomisierung
        random_fail = random.choice(edge_list)
        while random_fail in fails_list:
            random_fail = random.choice(edge_list)
        #randomisierung
        fails_list.append(random_fail)
    return fails_list


def get_fails_list_alt(g, source, destination, disjoint_path_list, fail_random, failure_num):
    edge_list = list(g.edges())
    pathList = disjoint_path_list[source][destination]
    num_edgedesjointpaths = len(pathList)
    fails_list = []
    if fail_random:
        for i in range(failure_num):
            random_fail = random.choice(edge_list)
            while random_fail in fails_list:
                random_fail = random.choice(edge_list)
            fails_list.append(random_fail)
    else:
        for i in range(num_edgedesjointpaths):
            nodeindex_in_path = random.randint(0, len(pathList[i])-2)
            fails_list.append((pathList[i][nodeindex_in_path], pathList[i][nodeindex_in_path+1]))
    return fails_list


#so viele fehler ins system bis kein weg mehr da ist 
#fehler auch auserhalb der kantendisjunkte pfade schmeißen sodass nicht nur 0-3 oder -7 vllt 0-40 
#mehr fehler ins systems schmeißen für 25 kanten : 10 oder 15 
#TODO: random graphen nehmen und edges set nutzen zwecks randomisierung.


# Modified SQ1 experiments function to work with loaded graph and output JSON
def sq1_experiments(g, failure_num, rep, filename):
    for i in range(rep):
        print('rep: ' + str(i))
        start_rep = time.time()
        nodes = list(g.nodes())
        n= len(nodes)
        edges = list(g.edges())
        resultHops = {}
        resultHopsShortCut = {}
        resultShortestPathForStretch = {}
        filename_json = 'results/zoo/' + filename + str(i) + '.json'
        for source in nodes:
            resultHops[source] = {}
            resultHopsShortCut[source] = {}
            resultShortestPathForStretch[source] = {}
            for destination in nodes:
                if source == destination:
                    continue
                disjoint_path_list = get_disjoint_path(g, destination)
                fails_list = get_fails_list_alt(g, source, destination, disjoint_path_list, False, failure_num)

                #fails_list = get_fails_list(g, source, destination, disjoint_path_list, failure_num)
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


            #print(resultHops)
            #print("VERSUS")
            #print(resultHopsShortCut)
            #print(resultShortestPathForStretch)
            #print(fails_list)
            #print(fails_sublist)
            #print(failure_num)

        # Prepare data for JSON serialization
        data_for_json = {
            "nodes": nodes,
            "edges": edges,
            "experiment_index": i,
            "resultShortestPathForStretch": resultShortestPathForStretch,
            "failure_num": failure_num,
            "resultHops": resultHops,
            "resultHopsShortCut": resultHopsShortCut
        }

        # Save as JSON
        with open(filename_json, 'w') as json_file:
            json.dump(data_for_json, json_file, indent=4)

        end_rep = time.time()
        print(time.asctime(time.localtime(start_rep)))
        print(time.asctime(time.localtime(end_rep)))



# Main execution
if __name__ == "__main__":
    start = time.time()
    print(time.asctime(time.localtime(start)))
    # Adjust the graph file path as needed
    #graph_file_path = '/home/mikheil/Desktop/SQ1_ShortCut-main/newdir/Gridnet_edited.gml'
    
    graph_file_path = '/home/mikheil/Desktop/SQ1_ShortCut-main/newdir/Noel_edited.gml'  
    filename =  os.path.basename(graph_file_path)
    g = load_graph(graph_file_path)
    # Parameters for experiments
    failure_num = 15 # Adjust as needed
    rep = 20  # Number of repetitions
    sq1_experiments(g, failure_num, rep, filename)
    end = time.time()
    print('Total execution time:', end - start)
    print(time.asctime(time.localtime(end)))
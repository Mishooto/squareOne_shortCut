import sys
import os 
from os import listdir, path, fsdecode
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools
from networkx.algorithms.connectivity import build_auxiliary_edge_connectivity
from networkx.algorithms.flow import build_residual_network
import random
import json
import time

#from obj_class_pickle import DataGraphs

# Function to load the graph from a GraphML file
def load_graph(file_path):
    return nx.read_graphml(file_path)  # Changed to read_graphml


def killedge(G,edge):
    """
    helper method for removing an edge, necessary because the built_in .remove_edge() function
    doesn't remove multiple vertices that may be present in a multigraph.
    """
    lst = [edge]
    edge2 = (edge[1],edge[0])
    lst.append(edge2)
    G.remove_edges_from(lst)

# SQ1 experiments
def sq1_experiments(n,k, rep, filename, gr, subname):
    for i in range(rep):
        print('rep: '+ str(i))
        start_rep = time.time()
        g = gr  # This now assumes gr is already a graph loaded from a GraphML file
        nodes = list(g.nodes())
        n= len(nodes)
        edges = list(g.edges())
        resultHops = {}
        resultHopsShortCut = {}
        resultShortestPathForStretch = {}
        filename_json = filename+"/" +subname+ str(i) + '.json'
        for source in nodes:
            resultHops[source] = {}
            resultHopsShortCut[source] = {}  
            resultShortestPathForStretch[source] = {}              
            for destination in nodes:
                if source == destination:
                    continue
                disjoint_path_list_nosc = get_disjoint_path(g, destination, fullrandom=True)
                fails_list, failedgraph= get_fails_list(g)        
                finalfails =len(fails_list)
                hop_list = []
                hop_list_shortcut = []
                dis_joint_path = disjoint_path_list_nosc[source][destination]
                dis_joint_path_shortcut = disjoint_path_list_nosc[source][destination]
                resultShortestPathForStretch[source][destination] = len(dis_joint_path[0])-1
                for j in range(0, len(fails_list)):
                    fails_sublist = fails_list[:j]
                    [_, hops, _, detour, _] = routingSQ1(dis_joint_path, source, destination, n, fails_sublist, failedgraph, sc_bool= False)
                    [_, hopsS, _, detourS, dis_joint_path_shortcut] = routingSQ1(dis_joint_path, source, destination, n, fails_sublist, failedgraph, sc_bool= True) 
                    hop_list.append(hops)
                    #print("nosc: ", hops, "sc: ", hopsS)
                    hop_list_shortcut.append(hopsS)
                resultHops[source][destination] = hop_list
                resultHopsShortCut[source][destination] = hop_list_shortcut
        data_for_json = {
            "nodes": nodes,
            "edges": edges,
            "experiment_index": i,
            "resultShortestPathForStretch": resultShortestPathForStretch,
            #"failure_num": failure_num,
            "failure_num": finalfails,
            "resultHops": resultHops,
            "resultHopsShortCut": resultHopsShortCut
        }
        # Save as JSON
        with open(filename_json, 'w') as json_file:
            json.dump(data_for_json, json_file, indent=4)
        end_rep = time.time()
        print(time.asctime( time.localtime(start_rep)))
        print(time.asctime( time.localtime(end_rep)))   

def get_fails_list(G):
    """
    helper method for generating the fails list. identifies cliques and bridges in a graph,
    severs all edges that are redundant for maintaining graph connectivity. from  identified clique_edges,
    bridges and any multiple vertices (from a multigraph) are filtered out, what's left is edges_toremove
    """
    fails_list=[]
    g= G.copy() 
    cliques = list(nx.find_cliques(g))
    #bridges = list(nx.bridges(g))
    edges = list(g.edges())
    for clique in cliques:
        # Create a subgraph of the clique, because 'clique' is an array not a graph
        clique_subgraph = g.subgraph(clique).copy()
        clique_edges = list(clique_subgraph.edges())
        #set_of_edges_toremove = set([x for x in clique_edges])
        #edges_toremove= []
        #for i in clique_edges:
        #    if i not in edges_toremove:
        #        edges_toremove.append(i)
        random.shuffle(clique_edges)
        for edge in clique_edges:
            randomedge = random.choice(clique_edges)
            #edges.remove(randomedge)
            killedge(g,edge)
            if not nx.is_connected(g):
            #if not assert_connectivity(g):
                g.add_edge(*edge)  # Add back the edge if removing it disconnects the graph
                #print("ADDBACK: ",edge)
            else:
                fails_list.append(edge)
    failedgraph = g
    return fails_list, failedgraph


#Create a list of edge-disjoint paths to destination, source nodes vary
def get_disjoint_path(g, destination, fullrandom = False):
    SQ1 = {}
    H = build_auxiliary_edge_connectivity(g)
    R = build_residual_network(H, 'capacity')
    SQ1 = {n: {} for n in g}
    for u in g.nodes():
        if (u != destination):
            if fullrandom:
                k = list(nx.edge_disjoint_paths(
                    g, u, destination, auxiliary=H, residual=R))
            else:
                k = sorted(list(nx.edge_disjoint_paths(
                    g, u, destination, auxiliary=H, residual=R)), key=len)
            SQ1[u][destination] = k
    return SQ1

#Check for fails in edge-disjoint paths
def doesntContainFail(path, fails):
    zipped = list(zip(path, path[1:]))
    return all(fail not in zipped for fail in fails)


#Routing
def routingSQ1(SQ1, source, destination, n, fails,g, sc_bool):
    print(f"")
    if sc_bool:
        #print(f"Original paths: {SQ1}")
        newList = [path for path in SQ1 if doesntContainFail(path, fails)]
        print(f"old Filtered paths: {newList} with the fails {fails}")
        if len(newList)<len(SQ1):
        #if len(newList) < 2:
        #if len(newList)
            restorepaths= get_disjoint_path(g, destination, fullrandom=True)
            newSQ1= restorepaths[source][destination]
            #SQ1= get_disjoint_path(g, destination, fullrandom=True)[source][destination]
            newnewList = [path for path in newSQ1 if doesntContainFail(path, fails)]
            for path in newnewList:
                if path not in newList:
                    newList.append(path)
                    print(f"newlist UPDATE: {path}")
        return (False, len(newList[0])-1, 2, None, newList)
    else:
        #SQ1= get_disjoint_path(g, destination, fullrandom=True)
        curRoute = SQ1[0]
        k = len(SQ1)
        detour_edges = []
        index = 1
        hops = 0
        n= len(list(g.nodes()))
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


# Main execution
if __name__ == "__main__":
    start = time.time()
    print(time.asctime( time.localtime(start)))
    n = 25
    rep = 10
    k = 8
    failure_num = 15
    ran_dom = True
    # Load the graph from "sago.graphml" directly here
    #fail_random = True
    #assert machen sind wir überhaupt immernoch connected
    #connected = pfad existiert
    directory_name = 'GraphMLZoo/archive'
    #fehler anzahl kantendisjunkte pfade -1 oder anzahl kanten bis knoten nicht mehr  
    #for file in os.listdir(directory_name):
    #    file = random.choice(os.listdir(directory_name))
    #    if file.endswith('.graphml'):
    #gr = load_graph("GraphMLZoo/Abvt.graphml")  # Make sure to update the path to where "sago.graphml" is located
    #filename = "Abvt"  # Assuming you're naming the experiments based on the graph file
    #print('start')
    #sq1_experiments(n, k, failure_num, rep, ran_dom, fail_random, filename, gr)
    graph_file_path = "GraphMLZoo/archive/Abvt.graphml"
    #graph_file_path = os.path.join(directory_name, file)
    filename_without_ext = os.path.splitext(os.path.basename(graph_file_path))[0]
    print(filename_without_ext)
    #TODO: Graphen fuer konnektivitaet pruefen vor iteration 
    dest = directory_name+"/results/"+filename_without_ext
    print(dest)
    if not os.path.exists(dest):
    # Create the directory
        os.makedirs(dest)
    gr = load_graph(graph_file_path)
    sq1_experiments(n,k, rep, dest, gr, filename_without_ext)
    print('ende')
    end = time.time()
    print('Total execution time:', end - start)
    print(time.asctime( time.localtime(end)))
    #TODO: commit machen und alles kommeentieren 
    #TODO: docstrings schreiben 
    #xval visaubrebt shortcutze
    #gtxov ghmerto gaaswore es fehleri rac maq 
    #da mere vcdi iteracias graphebze da davxedav rogor xdeba
    #da bonus points tu debuggershi davxedav ra xdeba
    # bonusbonus points tu gavasworeb am linearitaets rac scatterplotebshi sheinishneba
    # aseve sheinishneba line graphebis simetriulobashi cus ra xdeba there like 
    
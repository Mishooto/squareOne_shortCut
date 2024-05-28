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
from obj_class_pickle import DataGraphs



#TODO: number of failures shvidze rato wydeba? ramdenic ari magdenive anaxos,
#imis nacvlad ro concrete failure number mianicho, remove 1 kante, failurecount ++
#TODO: gaalamaze, gaiazre, randomize more, ecade ro update gaaketo after every fail
#TODO: fail scenario: network gaq  edgebi gaq, erti edge gamoakldeba edgebs, daemateba fails lists, tavidan gamoitvleba
#updated(shemcirebul) edges listze dafudznebit axali new minimum paths
#demo trial: gaakete 5 nodiani networki, 1 fehler daumate ise ro sheicvalos shortest pathi da naxe magaze dafudznebit rogor daaupdateo beliebige network sizeianebi.


#TODO: automatisiert über verzeichnis iterieren
#einzelne wiederholung linie als grafik statt boxplot, im linienform , wie viel hops man bis zum ziel braucht
#shortcut nicht nur am anfang, jede knoten im netzwerk und variationen davon , nur bei konnektivsten knoten anlegen gezielt 
#insgesamtgrafik machen iwie shortcut an 0 bis n knoten
#für graphergebnisse x achse anzahl scknoten y achse selbst überlegeen


# Function to load the graph from a GML file
def load_graph(file_path):
    return nx.read_gml(file_path)


#SQ1 experiments
def sq1_experiments(n, k, failure_num, rep, fail_random, filename, gr):   
    for i in range(rep):
        print('rep: '+ str(i))
        start_rep = time.time()
        #if fail_random:
        g = gr
        #else:
        #    g = create_graphs(n, k, i, 1)
        nodes = list(g.nodes())
        edges = list(g.edges())
        resultHops = {}
        resultHopsShortCut = {}
        resultShortestPathForStretch = {}
        #if fail_random:
        #    filename_pickle = 'results/workingzoo/' + 'SQ1_ShortCut_' + '_graph_' + str(ran_dom) + '_' + str(n) + '_' + str(len(edges)) + '_' + str(i) + '_' + str(fail_random) + '_' + str(failure_num) + '.pickle'
        #else:
        #    filename_json = 'results/workingzoo/' + filename + str(i) + '.json'
        #filename_json = 'results/workingzoo/'+filename+str(i)+'.json'
        filename_json= 'results/workingzoo/'+filename+str(i)+'.json'
        print(filename_json)
        for source in nodes:
            resultHops[source] = {}
            resultHopsShortCut[source] = {}  
            resultShortestPathForStretch[source] = {}              
            for destination in nodes:
                if source == destination:
                    continue
            
                #disjoint_path_list = get_disjoint_path(g, destination)
                disjoint_path_list = get_disjoint_path(g, destination, fullrandom=True)
                disjoint_path_list_shortcut = disjoint_path_list
                #fails_list = get_fails_list(g, source, destination, disjoint_path_list, True, failure_num)
                fails_list = get_fails_list(g, source, destination, disjoint_path_list, fail_random, failure_num)
                hop_list = []
                hop_list_shortcut = []
                dis_joint_path = disjoint_path_list_shortcut[source][destination]
                dis_joint_path_shortcut = dis_joint_path
                resultShortestPathForStretch[source][destination] = len(dis_joint_path[0])-1

                for j in range(0, len(fails_list)):
                    fails_sublist = fails_list[:j]
                    #update()
                    [_, hops, _, detour, _]= routingSQ1(dis_joint_path, source, destination, n, fails_sublist, sc_bool= False)
                    [_, hopsS, _, detourS, dis_joint_path_shortcut] = routingSQ1(dis_joint_path_shortcut, source, destination, n, fails_sublist, sc_bool= True) 
                    hop_list.append(hops)
                    hop_list_shortcut.append(hopsS)
                    #hop_list_shortcut.append(len(disjoint_path_list_shortcut[source][destination][j])-1)
                #hops_array = np.append(hops_array,[hop_list],axis=0)
                #hopsS_array = np.append(hopsS_array,[hop_list_shortcut],axis=0)
                # hops_list_rep.append(hop_list)
                # hops_list_shortcut_rep.append(hop_list_shortcut)
                #array2 = np.append(array,[liste], axis=0)
                resultHops[source][destination] = hop_list
                resultHopsShortCut[source][destination] = hop_list_shortcut
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
        print(time.asctime( time.localtime(start_rep)))
        print(time.asctime( time.localtime(end_rep)))   
        #toPickle = DataGraphs(seed, ran_dom, nodes, edges, i, resultShortestPathForStretch, fail_random, failure_num, resultHops, resultHopsShortCut) 

#Create a graph
def create_graphs(n, k, rep, seed):
    g = nx.random_regular_graph(k,n)
    while nx.edge_connectivity(g) < k: #Konnektivität von k oder größer, sonst neuen Graph erstellen
           g = nx.random_regular_graph(k, n).to_directed()
    g.graph['seed'] = seed
    # pickle.dump(g,  open( "./save.p", "wb" ))
    g.graph['k'] = k
    #with open('results/' + 'SQ1_ShortCut' + str(seed) + '_graph_' + str(n) + '_' + str(rep) + '.txt', 'w') as file:
        # file.write('n=' + str(n) + ', k=' + str(k) + ', rep=' + str(rep) + ', seed=' + str(seed)) 
        #file.write(f"{n=}, {k=}, {rep=}, {seed=}") 
    return g 

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

#def updateonce(g, s, d)
    ''' edge_list = list(g.edges())
    pathList = disjoint_path_list[source][destination]
    num_edgedesjointpaths = len(pathList)
    fails_list = []
    if fail_random:
        for i in range(failure_num):
            random_fail = random.choice(edge_list)
            while random_fail in fails_list:
                random_fail = random.choice(edge_list)
            fails_list.append(random_fail)'''

def update(g, source, destination):
    # Ensure a copy of the graph is used to avoid modifying the original graph
    g_modified = g.copy()
    disjoint_path_list = get_disjoint_path(g_modified, destination)
    while len(disjoint_path_list[source][destination]) > 1:
        # Randomly select a vertex that is not the source or destination
        nodes = list(set(g_modified.nodes()) - {source, destination})
        if not nodes:
            break  # Break if there are no nodes left to remove
        random_vertex = random.choice(nodes)
        
        # Remove the selected vertex from the graph
        g_modified.remove_node(random_vertex)
        
        # Recalculate the edge-disjoint paths with the updated graph
        disjoint_path_list = get_disjoint_path(g_modified, destination)
    
    return disjoint_path_list

#TODO: anzahl fehler geht nur bis 7, dynamisch erweitern 

#Create a list of fails, either random or specifically on edge-disjoint paths
def get_fails_list(g, source, destination, disjoint_path_list, fail_random, failure_num):
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

#Initialize parameters for experiments, take runtime, start experiments
if __name__ == "__main__":
    start = time.time()
    print(time.asctime( time.localtime(start)))
    n = 25
    rep = 10
    k = 8
    failure_num = 15
    ran_dom = True
    #fail_random False takes more computing time
    #fail_random = True
    fail_random = True
    #ran_dom = True
    #fail_random = False
    #G = nx.Graph()

    graph_file_path = '/home/mikheil/Desktop/SQ1_ShortCut-main/newdir/Abvt_edited.gml'  
    #filename =  os.path.basename(graph_file_path)
    #print(filename)
    gr = load_graph(graph_file_path)
    filename_without_ext = os.path.splitext(os.path.basename(graph_file_path))[0]
    print(filename_without_ext)
    print('start')
    sq1_experiments(n, k, failure_num, rep, fail_random, filename_without_ext, gr)
    print('ende')
    end = time.time()
    print('Total execution time:', end - start)
    print(time.asctime( time.localtime(end)))
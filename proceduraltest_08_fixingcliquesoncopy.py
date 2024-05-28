import networkx as nx
import matplotlib.pyplot as plt
import random


'''
import networkx as nx
import matplotlib.pyplot as plt

# Load the graph
G = nx.read_graphml('/home/mikheil/Desktop/SQ1_ShortCut-main/GraphMLZoo/archive/UniC.graphml')
original_graph = G.copy()  # Make a copy of the original graph for visualization

# Remove the edge (0, 1)
G.remove_edge('0', '1')
gnodes = list(G.edges())
GGnodes = list(original_graph.edges())
print (gnodes == GGnodes)
# Check if the graph is still connected
is_connected = nx.is_connected(G)
print("Graph is still connected:", is_connected)

# Visualization setup
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
pos = nx.spring_layout(original_graph)  # Use the same position for both plots for consistency

# Plot original graph
nx.draw(original_graph, pos, ax=axs[0], with_labels=True, node_color='skyblue', node_size=700, edge_color='k')
axs[0].set_title("Graph Before Edge Removal")

# Plot graph after edge removal
edge_colors = ['r' if edge == ('0', '1') or edge == ('1', '0') else 'k' for edge in G.edges()]
nx.draw(G, pos, ax=axs[1], with_labels=True, node_color='skyblue', node_size=700, edge_color=edge_colors)
axs[1].set_title("Graph After Edge Removal")

plt.show()

'''


def calculateEdgeDisjointPaths(G):
    """
    Calculates edge-disjoint paths for each pair of nodes where source is not equal to the destination.
    """
    edge_disjoint_paths = {}
    for source in G.nodes():
        for destination in G.nodes():
            if source != destination:
                try:
                    paths = list(nx.edge_disjoint_paths(G, source, destination))
                    edge_disjoint_paths[(source, destination)] = paths
                except nx.NetworkXNoPath:
                    edge_disjoint_paths[(source, destination)] = []
    return edge_disjoint_paths

def killedge(G,edge):
    lst = [edge]
    edge2 = (edge[1],edge[0])
    lst.append(edge2)
    G.remove_edges_from(lst)

def assertion(G):
    """
    Verifies if there exists at least one edge-disjoint path between every pair of distinct nodes in graph G
    using pre-calculated edge-disjoint paths.
    """
    edge_disjoint_paths = calculateEdgeDisjointPaths(G)
    for (source, destination), paths in edge_disjoint_paths.items():
        if len(paths) <= 1:
            return False
    return True

def random_fail(G):
    """
    Randomly selects an edge to fail in graph G while ensuring the graph remains connected.
    """
    edges = list(G.edges())
    random.shuffle(edges)
    for edge in edges:
        G.remove_edge(*edge)
        if nx.is_connected(G):
            return edge
        else:
            G.add_edge(*edge)
    return None

def remove_extraneous_edges_in_cliques(G, failslist):
    """
    Identifies all cliques in the graph and attempts to remove extraneous edges from them.
    """
    cliques = list(nx.find_cliques(G))
    for clique in cliques:
        # Create a subgraph of the clique
        clique_subgraph = G.subgraph(clique).copy()
        # List of edges in the clique subgraph
        clique_edges = list(clique_subgraph.edges())
        # Try to remove each edge in the clique subgraph
        for edge in clique_edges:
            print(edge)
            #G.remove_edge(*edge)
            killedge(G,edge)
            if not nx.is_connected(G):
            #if not assertion(G):
                G.add_edge(*edge)  # Add back the edge if removing it disconnects the graph
            else:
                failslist.append(edge)

# Parameters for random regular graph
#k = 4
#n = 8

k = 4
n = 16

# Generate a random regular graph
#G = nx.random_regular_graph(k, n)
#TODO: WASHALE ES ORI YLEOBA!!!!!
#G= nx.read_graphml('/home/mikheil/Desktop/SQ1_ShortCut-main/GraphMLZoo/archive/JanetExternal.graphml')
#G= nx.read_graphml('/home/mikheil/Desktop/SQ1_ShortCut-main/GraphMLZoo/archive/KentmanApr2007.graphml')
G= nx.read_graphml('/home/mikheil/Desktop/SQ1_ShortCut-main/GraphMLZoo/archive/KentmanAug2005.graphml')
G= nx.read_graphml('/home/mikheil/Desktop/SQ1_ShortCut-main/GraphMLZoo/archive/Garr201001.graphml')
#G= nx.read_graphml('/home/mikheil/Desktop/SQ1_ShortCut-main/GraphMLZoo/archive/KentmanJul2005.graphml')
#G= nx.read_graphml('/home/mikheil/Desktop/SQ1_ShortCut-main/GraphMLZoo/archive/Janetbackbone.graphml')
#G= nx.read_graphml('/home/mikheil/Desktop/SQ1_ShortCut-main/GraphMLZoo/archive/Bandcon.graphml')
#G= nx.read_graphml('/home/mikheil/Desktop/SQ1_ShortCut-main/GraphMLZoo/archive/Psinet.graphml')

#PROBLEM: Garr200908, Psinet, Garr201001 , janetbackbone, kentmanjul2005
original_graph = G.copy()  # Make a copy of the original graph for visualization
#G.remove_edge(*('0','1'))
print("ASSERTION: ",nx.is_connected(G))
# Calculate edge-disjoint paths before failing any edges
#print("Edge-Disjoint Paths:", calculateEdgeDisjointPaths(G))
#print("All nodes have at least one edge-disjoint path between them:", assertion(G))
print("CONNECTED K EDGES ")
#print(nx.is_k_edge_connected(G, k=1))
print("EDGEDISJOINTS: ",calculateEdgeDisjointPaths(G)[('0','1')])

fails = 0
failslist = []
x=0
while True:
    print("printingx")
    print(str(x))
    x+=1
    remove_extraneous_edges_in_cliques(G,failslist)
    failed_edge = random_fail(G)
    if failed_edge is None:
        break
    fails += 1
    if not assertion(G):
        break
print(failslist)
print("Total failures: ", len(failslist))

# Visualization setup
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
pos = nx.spring_layout(original_graph)  # Use the same position for both plots for consistency

# Plot original graph
nx.draw(original_graph, pos, ax=axs[0], with_labels=True, node_color='skyblue', node_size=700, edge_color='k')
axs[0].set_title("Graph Before Failures")

# Plot graph after failures
nx.draw(G, pos, ax=axs[1], with_labels=True, node_color='skyblue', node_size=700, edge_color='k')
axs[1].set_title("Graph After Failures")

plt.show()

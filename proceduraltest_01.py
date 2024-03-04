import networkx as nx
import matplotlib.pyplot as plt
import random




#NEW ansatz, s und d nehmen, aufm s-> pfad fehler schmeißen solange s->d connected 
# while s and d connected:
#     fehler auf sdpfad

#!s and d nicht mehr connected
#über die liste ausrechnen, wenn mindestens 1 element
#nach bridges gucken
#in jede iteration: wenn graph hat bridge und liegt aufm edge disjoint path dann ist 
#hasbridges() wenn keine bridges dann keine bridges()
#suche nach bridges
#y achse: hopes, x achse: kantendisjunkte pfade
#y kantendisjunkte pfade, x Fehler
# 
#wenn existiert bridge aufm pfad, bridge ist die kante die nicht gelöscht werden darf


#wie ändert sich die anzahl kantendisjunkte pfade nach fehler anzahl

def calculateEdgeDisjointPaths(G):
    """
    This function calculates edge-disjoint paths for each pair of source and destination nodes.
    Returns a dictionary with tuples of nodes as keys and lists of edge-disjoint paths as values.
    """
    edge_disjoint_paths = {}
    for source in G.nodes():
        for destination in G.nodes():
            if source != destination:
                try:
                    paths = list(nx.edge_disjoint_paths(G, source, destination))
                    edge_disjoint_paths[(source, destination)] = paths
                except nx.NetworkXNoPath:
                    # If there's no path between the nodes, we simply continue to the next pair
                    continue
    return edge_disjoint_paths

def visualize_differences(before, after, failed_edge):
    """
    This function finds the differences in edge-disjoint paths caused by a failure.
    It now only considers paths that included the failed edge and omits empty lists.
    """
    removed_paths = {}
    for key in before:
        if key not in after or before[key] != after[key]:
            removed_paths_with_edge = [path for path in before[key] if failed_edge in zip(path, path[1:])]
            if removed_paths_with_edge:  # Only add to the dictionary if the list is not empty
                removed_paths[key] = removed_paths_with_edge
    print("Removed edge-disjoint paths after failure:", removed_paths)


def random_fail(G):
    """
    This function selects a random edge from the graph and marks it for failure.
    Returns the graph with the failed edge marked.
    """
    if len(G.edges()) == 0:
        return None  # Return None if the graph has no edges to fail
    # Select a random edge
    failed_edge = random.choice(list(G.edges()))
    return failed_edge

# Generate a random graph with given constraints
k = 4
n = 6
#k=3
#n=10
G = nx.random_regular_graph(k, n)
while nx.edge_connectivity(G) < k:  # Ensure connectivity of k
    G = nx.random_regular_graph(k, n)

# Calculate edge-disjoint paths before failure
before_failure_paths = calculateEdgeDisjointPaths(G)

# Introduce a random failure to the network
failed_edge = random_fail(G)

# Remove the failed edge from the graph
if failed_edge:
    G.remove_edge(*failed_edge)
    after_failure_paths = calculateEdgeDisjointPaths(G)
    visualize_differences(before_failure_paths, after_failure_paths, failed_edge)

# Calculate edge-disjoint paths after failure
#after_failure_paths = calculateEdgeDisjointPaths(G)

# Visualize the differences between edge-disjoint paths before and after the failure
#visualize_differences(before_failure_paths, after_failure_paths)

# Draw the graph
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='k')
if failed_edge:
    # Draw the failed edge in red
    nx.draw_networkx_edges(G, pos, edgelist=[failed_edge], edge_color='r', width=2)

plt.show()

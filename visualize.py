import networkx as nx
import matplotlib.pyplot as plt
import random
from networkx.algorithms.connectivity import build_auxiliary_edge_connectivity
from networkx.algorithms.flow import build_residual_network


# Path to the GML file
#graph_file_path = '/home/mikheil/Desktop/SQ1_ShortCut-main/newdir/Aconet_edited.gml'
#graph_file_path = '/home/mikheil/Desktop/SQ1_ShortCut-main/newdir/Uran_edited.gml'
#graph_file_path = '/home/mikheil/Desktop/SQ1_ShortCut-main/newdir/Noel_edited.gml'
graph_file_path = '/home/mikheil/Desktop/SQ1_ShortCut-main/newdir/Niif_edited.gml'
# Function to load and visualize the graph
def visualize_graph(file_path):
    # Load the graph from the GML file
    g = nx.read_gml(file_path)
    
    # Output basic information about the graph
    print("Number of nodes:", g.number_of_nodes())
    print("Number of edges:", g.number_of_edges())
    # Create a plot
    plt.figure(figsize=(12, 8))
    # Draw the graph
    pos = nx.spring_layout(g)  # positions for all nodes
    nx.draw(g, pos, with_labels=False, node_color='skyblue', node_size=500, edge_color='gray')
    # Draw labels separately to control their position
    label_pos = {k: [v[0], v[1] - 0.05] for k, v in pos.items()}  # Offset the y-position for labels
    nx.draw_networkx_labels(g, label_pos)
    # Show the plot
    plt.title("Graph Visualization")
    plt.show()

# Call the function with the provided file path
#visualize_graph(graph_file_path)

def visualize_random_paths(file_path, times=5):
    # Load the graph from the GML file
    g = nx.read_gml(file_path)
    
    # Ensure the graph is connected to find a path
    if not nx.is_connected(g):
        print("Graph is not connected. Finding paths in the largest connected component.")
        g = max(nx.connected_components(g), key=len)
        g = g.subgraph(c).copy()

    # Set up the plot grid
    fig, axes = plt.subplots(1, times, figsize=(20, 4))
    
    for i in range(times):
        ax = axes[i]
        # Select random source and destination
        nodes = list(g.nodes())
        source = random.choice(nodes)
        destination = source
        while destination == source:
            destination = random.choice(nodes)

        # Find a path between the source and destination
        try:
            path = nx.shortest_path(g, source=source, target=destination)
        except nx.NetworkXNoPath:
            ax.set_title('No Path')
            continue

        # Draw the full graph lightly in the background
        pos = nx.spring_layout(g, seed=42)  # For consistent layout across subplots
        nx.draw(g, pos, ax=ax, with_labels=False, node_color='lightgray', node_size=50, edge_color='lightgray')

        # Highlight the path
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(g, pos, nodelist=path, node_color='skyblue', node_size=100, ax=ax)
        nx.draw_networkx_edges(g, pos, edgelist=path_edges, edge_color='red', width=2, ax=ax)

        ax.set_title(f'Path {i+1}\n{source}->{destination}')

    plt.tight_layout()
    plt.show()

# Call the function with the provided file path
#visualize_random_paths(graph_file_path, times=5)














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

#####ANALYSIS ONGOING!!!!!!!!!############################################



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




def get_fails_list(g, source, destination, disjoint_path_list, failure_num):
    edge_list = list(g.edges())
    pathList = disjoint_path_list[source][destination]
    num_edgedisjointpaths = len(pathList)
    max_fails = min(failure_num, num_edgedisjointpaths - 1)
    fails_list = []
    for _ in range(max_fails):
        random_fail = random.choice(edge_list)
        while random_fail in fails_list:
            random_fail = random.choice(edge_list)
        fails_list.append(random_fail)
    return fails_list



#####COPYZONE!!!!! 2 B ERADICATED !!!!!!!!!!!###########################

def analyzesinglerep():
    g = nx.read_gml('/home/mikheil/Desktop/SQ1_ShortCut-main/newdir/Noel_edited.gml')
    failure_num=27
    rep = 0 
    nodes = list(g.nodes())
    n= len(nodes)
    edges = list(g.edges())
    resultHops = {}
    resultHopsShortCut = {}
    resultShortestPathForStretch = {}
    for source in nodes:
        resultHops[source] = {}
        resultHopsShortCut[source] = {}
        resultShortestPathForStretch[source] = {}
        for destination in nodes:
            if source == destination:
                continue
            disjoint_path_list = get_disjoint_path(g, destination)
            fails_list = get_fails_list(g, source, destination, disjoint_path_list, failure_num)
    if 'P' in source:
        print(disjoint_path_list)

#analyzesinglerep()

    


def visualize_disjoint_paths(file_path, times=3):
    # Load the graph from the GML file
    g = nx.read_gml(file_path)
    
    # Ensure the graph is connected to find a path
    if not nx.is_connected(g):
        print("Graph is not connected. Finding paths in the largest connected component.")
        g = max(nx.connected_components(g), key=len)
        g = g.subgraph(c).copy()

    # Set up the plot grid
    fig, axes = plt.subplots(1, times, figsize=(20, 4))
    
    nodes = list(g.nodes())
    source = random.choice(nodes)
    print(source)

    destination = source
    while destination == source:
        destination = random.choice(nodes)
    print(destination)

    disjoint_path_list = get_disjoint_path(g, destination)
    print(disjoint_path_list)
    for i in range(times):
        ax = axes[i]
        # Select random source and destination
        # Find a path between the source and destination
        try:
            choices = disjoint_path_list[source][destination]
            print("INDEX")
            print(choices)
            #print(index)
            choice = random.choice(choices)
            choices=choices.remove(choice)
            path = choice
            #index = random.randint(0,len(choices))
            #path=min(choices[index], len(choices))
            #choices = choices.pop(index)
            #path = nx.shortest_path(g, source=source, target=destination)
        except nx.NetworkXNoPath:
            print("NOPATH")
            ax.set_title('No Path')
            continue

        # Draw the full graph lightly in the background
        pos = nx.spring_layout(g, seed=42)  # For consistent layout across subplots
        nx.draw(g, pos, ax=ax, with_labels=False, node_color='lightgray', node_size=50, edge_color='lightgray')

        # Highlight the path
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(g, pos, nodelist=path, node_color='skyblue', node_size=100, ax=ax)
        nx.draw_networkx_edges(g, pos, edgelist=path_edges, edge_color='red', width=2, ax=ax)

        ax.set_title(f'Path {i+1}\n{source}->{destination}')

    plt.tight_layout()
    plt.show()

# Call the function with the provided file path
visualize_disjoint_paths(graph_file_path, times=2)

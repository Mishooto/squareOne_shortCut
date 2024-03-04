import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random


def display_graph_before_after_changes():
    # Create an example graph
    G = nx.cycle_graph(5)
    pos = nx.spring_layout(G, seed=42)  # Fixed layout for consistency

    # Display the original graph
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)  # 1 row, 2 columns, first subplot
    nx.draw(G, pos, with_labels=True, node_color='skyblue')
    plt.title("Original Graph")

    # Apply changes to the graph (e.g., adding a node and connecting it)
    G.add_node(5)
    G.add_edge(0, 5)
    G.add_edge(5, 3)

    # Recalculate positions to include the new node
    pos = nx.spring_layout(G, seed=42)  # Recalculate layout including the new node

    # Display the modified graph
    plt.subplot(1, 2, 2)  # 1 row, 2 columns, second subplot
    nx.draw(G, pos, with_labels=True, node_color='lightgreen')
    plt.title("Modified Graph")

    plt.show()

# Run the function to display the graphs
#display_graph_before_after_changes()


def epicfail():
    # Load your graph
    graph_file_path = '/home/mikheil/Desktop/SQ1_ShortCut-main/newdir/Noel_edited.gml'  # Update this path
    g = nx.read_gml(graph_file_path)

    # Ensure the graph is connected to find a path
    if not nx.is_connected(g):
        largest_cc = max(nx.connected_components(g), key=len)
        g = g.subgraph(largest_cc).copy()

    fig, ax = plt.subplots()

    pos = nx.spring_layout(g, seed=42)  # For consistent layout

    # Initial drawing of the graph
    nx.draw(g, pos, ax=ax, with_labels=True)

    class GraphUpdater:
        def __init__(self, graph, pos):
            self.graph = graph
            self.pos = pos
            self.edges = list(graph.edges())

        def insert_failure(self, event):
            if self.edges:
                # Randomly select an edge
                failed_edge = random.choice(self.edges)
                self.edges.remove(failed_edge)  # Remove from the list to avoid re-selection

                # Highlight the failed edge in red
                nx.draw_networkx_edges(self.graph, self.pos, edgelist=[failed_edge], width=2, edge_color='red')
                plt.draw()

    updater = GraphUpdater(g, pos)

    # Create the button
    axcut = plt.axes([0.7, 0.05, 0.2, 0.075])
    btn = Button(axcut, 'Insert Random Failure')

    # Link button event
    btn.on_clicked(updater.insert_failure)
    plt.show()


epicfail()




## list of edge disjoint paths from u to destination: SQ1[u][destination]
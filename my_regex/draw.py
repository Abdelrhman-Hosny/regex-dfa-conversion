import networkx as nx
import matplotlib.pyplot as plt
from IPython.display import Image

options = {
    "font_size": 36,
    "node_size": 3000,
    "node_color": "white",
    "edgecolors": "white",
    "linewidths": 1,
    "width": 1,
}


def draw_states(state_dict):
    G = nx.MultiDiGraph()
    for pointing_node, v in state_dict.items():
        if pointing_node == "startingState":
            continue
        for node_input, v1 in v.items():
            if node_input == "acceptingState":
                continue
            for pointed_to_node in v1:
                G.add_edge(pointing_node, pointed_to_node, label=node_input)

    nx.drawing.nx_pydot.write_dot(G, 'multi.dot')
import networkx as nx
from subprocess import check_call
from PIL import Image

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
                G.nodes[pointing_node]["shape"] = "doublecircle"
                continue
            for pointed_to_node in v1:
                G.add_edge(pointing_node, pointed_to_node, label=node_input)

    nx.drawing.nx_pydot.write_dot(G, "nfa.dot")
    # (graph,) = pydot.graph_from_dot_file('nfa.dot')
    # graph.write_png('nfa.png')

    check_call(['dot','-Tpng','nfa.dot','-o','nfa.png'])
    img = Image.open("nfa.png")
    img.show()

def draw_states_dfa(states_dict, accepting_states, name="dfa"):
    G = nx.MultiDiGraph()
    for pointing_node, v in states_dict.items():
        if pointing_node == "startingState":
            continue
        for node_input, pointed_to_node in v.items():
            if node_input == "acceptingState":
                continue
            G.add_edge(pointing_node, pointed_to_node, label=node_input)

    for node in accepting_states:
        G.nodes[node]["shape"] = "doublecircle"
    nx.drawing.nx_pydot.write_dot(G, name + ".dot")
    check_call(['dot','-Tpng',f'{name}.dot','-o',f'{name}.png'])
    # (graph,) = pydot.graph_from_dot_file(name + ".dot")
    # graph.write_png(name + ".png")
    img = Image.open(f"{name}.png")
    img.show()

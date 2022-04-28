import networkx as nx

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


def draw_states_dfa(states_dict, accepting_states, name="dfa"):
    G = nx.DiGraph()
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

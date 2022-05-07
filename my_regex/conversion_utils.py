import json


def add_key_val_dfa(DFA, key1, key2, val):
    if not DFA.get(key1):
        DFA[key1] = {}
    if not DFA[key1].get(key2):
        DFA[key1][key2] = val
    return DFA


def write_dfa_to_json(d, filename):
    with open(filename, "w") as f:
        json.dump(d, f)

def read_json(filename):

    with open(filename, "r") as f:
        state_dict = json.load(f)
    return state_dict



def rename_dfa(dfa, accepting_states, start_state):

    increment = 0
    visited = set()
    name_dict = {}
    new_dfa = {}

    for state1, transitions in dfa.items():
        if state1 not in visited:
            visited.add(state1)
            name_dict[state1] = increment
            increment += 1
        for input_char, state2 in transitions.items():
            if state2 not in visited:
                visited.add(state2)
                name_dict[state2] = increment
                increment += 1

    accepting_states = {name_dict[state] for state in accepting_states}
    start_state = name_dict[start_state]

    for state1, transitions in dfa.items():
        new_dfa[name_dict[state1]] = {}
        for input_char, state2 in transitions.items():
            new_dfa[name_dict[state1]][input_char] = name_dict[state2]

    new_dfa["startingState"] = start_state

    return new_dfa, accepting_states

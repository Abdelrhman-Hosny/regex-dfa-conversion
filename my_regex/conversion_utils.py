def add_key_val_dfa(DFA, key1, key2, val):
    if not DFA.get(key1):
        DFA[key1] = {}
    if not DFA[key1].get(key2):
        DFA[key1][key2] = val
    return DFA


def rename_dfa(dfa):

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

    for state1, transitions in dfa.items():
        new_dfa[name_dict[state1]] = {}
        for input_char, state2 in transitions.items():
            new_dfa[name_dict[state1]][input_char] = name_dict[state2]

    return new_dfa

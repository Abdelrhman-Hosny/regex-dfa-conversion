def get_inputs_and_non_acc_states(state_dict, accepting_states):

    non_accepting_states = set()
    dfa_inputs = set()
    for state1, v in state_dict.items():
        if state1 == "startingState":
            continue
        if state1 not in accepting_states:
            non_accepting_states.add(state1)
        for input_char, state2 in v.items():
            if state2 not in accepting_states:
                non_accepting_states.add(state2)
            if input_char not in dfa_inputs:
                dfa_inputs.add(input_char)

    return non_accepting_states, dfa_inputs


class MySet:
    def __init__(self, my_set) -> None:
        self.my_set = my_set
        if self.my_set:
            self.representative = next(iter(self.my_set))
        else:
            self.representative = None

    def contains(self, item):
        return item in self.my_set

    def __len__(self):
        return len(self.my_set)

    def reset_representative(self):
        self.representative = next(iter(self.my_set)) if self.my_set else None

    def get_list(self):
        return list(self.my_set)

    def __iter__(self):
        return iter(self.my_set)


def get_groups(state_dict, TT, dfa_inputs):

    while True:
        no_change = True

        for state_set in TT:
            if len(state_set) == 1:
                continue
            for dfa_input in dfa_inputs:
                outputs = []
                for state1 in state_set.my_set:
                    outputs.append(state_dict[state1].get(dfa_input, None))

                state_destination = []
                for output in outputs:
                    if output is None:
                        state_destination.append(None)
                        continue
                    for state2 in TT:
                        if state2.contains(output):
                            state_destination.append(state2.representative)
                            break
                if len(set(state_destination)) == 1:
                    continue
                else:
                    set_dict = {x: set() for x in state_destination}
                    for state, destination in zip(state_set, state_destination):
                        set_dict[destination].add(state)
                    TT.remove(state_set)
                    for state, destination in set_dict.items():
                        TT.append(MySet(destination))
                    no_change = False
                    break

        if no_change:
            break

    return TT


def minimize_dfa(state_dict, accepting_states):
    """
    Returns a minimized DFA
    """

    non_accepting_states, dfa_inputs = get_inputs_and_non_acc_states(
        state_dict, accepting_states
    )

    TT = get_groups(
        state_dict, [MySet(non_accepting_states), MySet(accepting_states)], dfa_inputs
    )

    TT = [x for x in TT if len(x) > 1]

    renaming_dict = {}
    for group in TT:
        for state in group:
            renaming_dict[state] = group.representative

    new_dfa = {}
    for state, v in state_dict.items():
        if state == "startingState":
            new_dfa["startingState"] = renaming_dict.get(state, state)
        else:
            new_dfa[renaming_dict.get(state, state)] = {}
            for input_char, state2 in v.items():
                new_dfa[renaming_dict.get(state, state)][
                    input_char
                ] = renaming_dict.get(state2, state2)

    return new_dfa, {renaming_dict.get(state, state) for state in accepting_states}

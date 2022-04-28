from my_regex import EPSILON
from collections import deque
from copy import deepcopy


def convert_to_dfa(states_dict):

    start_state_nfa = states_dict["startingState"]
    start_state = epsilon_closure(deque([start_state_nfa]), states_dict)

    print(start_state)
    return epsilon_closure(deque(move(start_state, 'b', states_dict)), states_dict)


def epsilon_closure(states, states_dict):
    """
    Finds the epsilon closure of a state.
    """

    visited_states = set()

    while states:
        current_state = states.popleft()
        visited_states.add(current_state)

        for state in states_dict[current_state].get(EPSILON, []):
            if state not in visited_states:
                states.append(state)

    return visited_states


def move(states, char, states_dict):
    """returns all states reachable from each state on char"""
    next_states = set()
    for state in states:
        next_states = next_states.union(states_dict[state].get(char, set()))

    return next_states


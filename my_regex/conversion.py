from my_regex import EPSILON
from my_regex.conversion_utils import add_key_val_dfa, rename_dfa


def convert_to_dfa(states_dict):

    start_state_nfa = states_dict["startingState"]
    start_state = epsilon_closure([start_state_nfa], states_dict)

    DFA, accepting_states = generate_dfa(start_state, states_dict)

    return rename_dfa(DFA, accepting_states, frozenset(start_state))


def generate_dfa(start_state, states_dict):

    dfa = {}
    accepting_states = set()
    states_queue = [frozenset(start_state)]
    visited_states = set()
    while states_queue:
        current_states = states_queue.pop()
        visited_states.add(current_states)

        moves = get_all_moves(current_states, states_dict)
        for k, v in moves.items():
            if k == "acceptingState":
                accepting_states.add(current_states)
                continue
            moves[k] = epsilon_closure(v, states_dict)
            add_key_val_dfa(dfa, current_states, k, frozenset(moves[k]))
            if frozenset(moves[k]) not in visited_states:
                states_queue.append(frozenset(moves[k]))

    return dfa, accepting_states


def epsilon_closure(states, states_dict):
    """
    Finds the epsilon closure of a state.
    """

    states_list = list(states)
    visited_states = set()

    while states_list:
        current_state = states_list.pop()
        visited_states.add(current_state)

        for state in states_dict[current_state].get(EPSILON, []):
            if state not in visited_states:
                states_list.append(state)

    return visited_states


def move(states, char, states_dict):
    """returns all states reachable from each state on char"""
    next_states = set()
    for state in states:
        next_states = next_states.union(states_dict[state].get(char, set()))

    return next_states


def get_all_moves(states, states_dict):

    moves = {}
    for state in states:
        for char_input in states_dict[state].keys():
            if char_input != EPSILON:
                moves[char_input] = moves.get(char_input, set()).union(
                    states_dict[state][char_input]
                )

    return moves

from my_regex.conversion import convert_to_dfa
from my_regex.utils import (
    write_dict_to_json,
    write_dfa_to_json,
    add_key_val,
)

from my_regex.draw import draw_states, draw_states_dfa

from my_regex.operators import get_regex


def construct_nfa(regex):
    """
    Construct an NFA from a regex.
    """
    NFA = {0: {}}

    current_state, NFA = get_regex(regex, NFA, 0)
    add_key_val(NFA, current_state, 'acceptingState', True)
    NFA["startingState"] = 0
    return NFA


NFA = construct_nfa("ba*|b+|a?")
DFA = convert_to_dfa(NFA)
write_dict_to_json(NFA, "nfa.json")
write_dfa_to_json(DFA, "dfa.json")
# print(NFA)
draw_states(NFA)
draw_states_dfa(DFA)

from my_regex.conversion import convert_to_dfa
from my_regex.minimization import minimize_dfa
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


# NFA = construct_nfa("(AB|C[A-Z])+")
NFA = construct_nfa("(((AB)|C)[A-Z])+")
print(f"NFA:\n{NFA}")
DFA, accepting_states_dfa = convert_to_dfa(NFA)
print(f'DFA:\n{DFA}')
minimized_DFA, accepting_states_dfa_min = minimize_dfa(DFA, accepting_states_dfa)
write_dict_to_json(NFA, "nfa.json")
write_dfa_to_json(DFA, "dfa.json")
write_dfa_to_json(minimized_DFA, "minimized_dfa.json")
# print(NFA)
draw_states(NFA)
draw_states_dfa(DFA, accepting_states_dfa)
draw_states_dfa(minimized_DFA, accepting_states_dfa_min, "dfa_min")

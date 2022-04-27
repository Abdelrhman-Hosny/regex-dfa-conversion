from my_regex.utils import (
    write_dict_to_json,
    get_num_of_last_state,
    add_key_val,
    detect_or_positions
)

from my_regex.draw import draw_states

from my_regex.operators import get_regex


def construct_nfa(regex):
    """
    Construct an NFA from a regex.
    """
    NFA = {"S0": {}}

    current_state, NFA = get_regex(regex, NFA, 0)

    add_key_val(NFA, f'S{get_num_of_last_state(NFA)}', 'acceptingState', True)
    NFA["startingState"] = "S0"
    return NFA


NFA = construct_nfa("ab+|cd|ef")
write_dict_to_json(NFA, "nfa.json")
print(NFA)
draw_states(NFA)

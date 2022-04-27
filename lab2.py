from my_regex.utils import (
    write_dict_to_json,
    add_key_val,
)

from my_regex.draw import draw_states

from my_regex.operators import get_regex


def construct_nfa(regex):
    """
    Construct an NFA from a regex.
    """
    NFA = {"S0": {}}

    current_state, NFA = get_regex(regex, NFA, 0)
    add_key_val(NFA, f'S{current_state}', 'acceptingState', True)
    NFA["startingState"] = "S0"
    return NFA


NFA = construct_nfa("ba*|b+|a?")
# NFA = construct_nfa("bs|(eb)*|a")
write_dict_to_json(NFA, "nfa.json")
print(NFA)
draw_states(NFA)

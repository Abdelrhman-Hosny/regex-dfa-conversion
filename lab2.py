from my_regex.utils import (
    write_dict_to_json,
    get_num_of_last_state
)

from my_regex.draw import draw_states

from my_regex.operators import get_regex


def construct_nfa(regex):
    """
    Construct an NFA from a regex.
    """
    NFA = {"S0": {}}

    current_state, NFA = get_regex(regex, NFA, 0)

    NFA[f"S{get_num_of_last_state(NFA)}"] = {"acceptingState": True}
    NFA["startingState"] = "S0"
    return NFA


NFA = construct_nfa("[ab]*")
print(NFA)
draw_states(NFA)
# print(construct_nfa("([qs])([wqeqwdwq])"))
# print(construct_nfa("a(((ys)(we))(xp))c"))
# print(zero_or_more("ab", {"S0": {}}, 0))
# print(optional("(ab)*", {"S0": {}}, 0))

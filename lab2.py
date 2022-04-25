from my_regex import EPSILON
from my_regex.utils import (
    write_dict_to_json,
    get_matched_parenthesis,
    get_matched_square_brackets,
    validate_brackets,
    validate_sorted_brackets,
    get_containing_brackets,
)

reg = "abc"


def set_alnum_state(char, NFA, current_state, next_state):
    nfa_keys = NFA.keys()
    if current_state not in nfa_keys:
        NFA[current_state] = {}
    if next_state not in nfa_keys:
        NFA[next_state] = {}
    NFA[current_state][char] = next_state


def get_next_brackets(regex, brackets):
    if not brackets:
        return None, None
    try:
        (outer_bracket, inner_brackets) = next(brackets)
        return remove_unnessasary_brackets(regex, outer_bracket, inner_brackets)
    except StopIteration:
        return None, None


def construct_nfa(regex):
    """
    Construct an NFA from a regex.
    """
    NFA = {"startingState": "S0", "S0": {}}

    current_state = get_regex(regex, NFA, 0)

    NFA[f'S{current_state}'] = {"acceptingState": True}
    return NFA


def get_brackets(regex):

    brackets = get_matched_square_brackets(regex) +\
         get_matched_parenthesis(regex)

    brackets = sorted(brackets, key=lambda x: x[0])
    validate_sorted_brackets(brackets)

    return (x for x in get_containing_brackets(brackets))


def get_regex(regex, NFA, current_state, in_brackets=False):

    i = 0

    brackets = get_brackets(regex)
    (current_outer_bracket, current_inner_brackets) = get_next_brackets(regex, brackets)
    while i < len(regex):
        # checking for alnum
        for char in regex[i:]:
            # if char is alphanumeric, we add the transition else break
            if not char.isalnum():
                break
            set_alnum_state(char, NFA,
                            f"S{current_state}", f"S{current_state + 1}")

            if not (in_brackets and not current_outer_bracket):
                current_state += 1
            i += 1

        # checking for brackets
        if current_outer_bracket and i == current_outer_bracket[0]:
            # we are at the start of the outer bracket
            current_state = get_regex(regex[i + 1:current_outer_bracket[1]], NFA, current_state, True)

            i = current_outer_bracket[1] + 1
            (current_outer_bracket, current_inner_brackets) = get_next_brackets(regex, brackets)
            current_state += 1

    return current_state


# play_dict = {
#     "name": {"first": "Alice", "last": "Wonderland"},
#     "description": "play a game",
#     "usage": "play [game]",
# }
# write_dict_to_json(play_dict, "play.json")
def remove_unnessasary_brackets(regex, outer_bracket, inner_brackets):
    s1, e1 = outer_bracket
    num_removed = i = 0

    while i < len(inner_brackets):
        s2, e2 = inner_brackets[i]
        if s2 - s1 == 1 + num_removed and e1 - e2 == 1 + num_removed:
            num_removed += 1
            inner_brackets.remove((s2, e2))
            regex = regex[:e2] + regex[e2 + 1:]
            regex = regex[:s2] + regex[s2 + 1:]
        else:
            i += 1
    return (outer_bracket, inner_brackets)


def zero_or_more(regex, NFA, current_state, regex_fn=get_regex):

    NFA[f'S{current_state}'][EPSILON] = [f'S{current_state + 1}']
    current_state += 1
    start_state = current_state
    new_state = get_regex(regex, NFA, start_state)
    NFA[f'S{start_state}'][EPSILON] = [f'S{new_state + 1}']

    NFA[f'S{new_state}'][EPSILON] = [f'S{start_state}']
    NFA[f'S{new_state}'][EPSILON].append(f'S{new_state + 1}')

    return new_state + 1, NFA


# print(construct_nfa("([qs])([wqeqwdwq])"))
# print(construct_nfa("ax((((ys)(we))))ac"))
# print(zero_or_more('ab', {"S0": {}}, 0))

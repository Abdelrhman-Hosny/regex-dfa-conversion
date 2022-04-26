from my_regex import EPSILON
from my_regex.utils import (
    add_key_val,
    get_brackets,
    get_next_brackets,
    detect_empty_nfa,
    get_num_of_last_state,
)


def get_regex(regex, NFA, current_state, in_brackets=False, bracket_type=None):

    i = 0

    brackets = get_brackets(regex)
    (current_outer_bracket, current_inner_brackets) = get_next_brackets(regex, brackets)
    while i < len(regex):
        # checking for alnum
        for char in regex[i:]:
            # if char is alphanumeric, we add the transition else break
            if not char.isalnum():
                break

            if (i+1) < len(regex) and regex[i+1] in regex_operators.keys():
                current_state, _ = regex_operators[regex[i+1]](char, NFA, current_state, regex_fn=get_regex)
                i += 1
            else:
                set_alnum_state(char, NFA, f"S{current_state}", f"S{current_state + 1}")

            if bracket_type == '(' or bracket_type is None:
                current_state += 1
            i += 1
        if bracket_type == '[':
            current_state += 1
        # checking for brackets
        if current_outer_bracket and i == current_outer_bracket[0]:

            if (i+1) < len(regex) and regex[current_outer_bracket[1] + 1] in regex_operators.keys():
                current_state, new_NFA = regex_operators[regex[current_outer_bracket[1] + 1]](regex[i+1: current_outer_bracket[1]], NFA, current_state, bracket_type=regex[i], regex_fn=get_regex)
                i = current_outer_bracket[1] + 2
            else:
                # we are at the start of the outer bracket
                current_state, new_NFA = get_regex(
                    regex[i + 1: current_outer_bracket[1]],
                    {f"S{current_state}": {}},
                    current_state,
                    True,
                )
                i = current_outer_bracket[1] + 1
            if detect_empty_nfa(NFA):
                NFA = new_NFA
                current_state = get_num_of_last_state(NFA) + 1

            elif not detect_empty_nfa(new_NFA):
                NFA = {**NFA, **new_NFA}
                current_state = get_num_of_last_state(NFA) + 1

            (current_outer_bracket, current_inner_brackets) = get_next_brackets(
                regex, brackets
            )


    return current_state, NFA


def zero_or_more(regex, NFA, current_state, bracket_type=None, regex_fn=get_regex):

    add_key_val(NFA, f"S{current_state}", EPSILON, f"S{current_state + 1}")
    current_state += 1
    start_state = current_state
    new_state, new_NFA = regex_fn(regex, NFA, start_state, bracket_type=bracket_type)
    
    add_key_val(NFA, f"S{start_state}", EPSILON, f"S{new_state + 1}")
    add_key_val(NFA, f"S{new_state}", EPSILON, f"S{start_state}")
    add_key_val(NFA, f"S{new_state}", EPSILON, f"S{new_state + 1}")
    NFA[f"S{new_state + 1}"] = dict()
    NFA = {**NFA, **new_NFA}
    return new_state, NFA


def set_alnum_state(char, NFA, current_state, next_state):
    add_key_val(NFA, current_state, char, next_state)


def optional(regex, NFA, current_state, bracket_type=None, regex_fn=get_regex):
    start_state = current_state
    current_state, NFA = regex_fn(regex, NFA, current_state, bracket_type=bracket_type)
    add_key_val(NFA, f"S{start_state}", EPSILON, f"S{current_state}")
    return current_state, NFA

def one_or_more(regex, NFA, current_state, regex_fn=get_regex):
    pass


regex_operators = {
    "*": zero_or_more,
    "?": optional,
    "+": one_or_more
}

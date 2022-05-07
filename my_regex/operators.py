from my_regex import EPSILON, ESCAPED_CHARS
from my_regex.utils import (
    add_key_val,
    get_brackets,
    get_next_brackets,
    get_split_indices_for_or_operation,
)

def construct_nfa(regex):
    """
    Construct an NFA from a regex.
    """
    NFA = {0: {}}

    current_state, NFA = get_regex(regex, NFA, 0)
    add_key_val(NFA, current_state, 'acceptingState', True)
    NFA["startingState"] = 0
    return NFA



def get_regex(regex, NFA, current_state, in_brackets=False, bracket_type=None):

    i = 0

    start_state = current_state

    split_indices = get_split_indices_for_or_operation(regex)

    if split_indices:
        split_indices = [-1] + split_indices
        split_indices.append(len(regex) + 1)

        new_split_indices = [
            (split_indices[i], split_indices[i + 1])
            for i in range(len(split_indices) - 1)
        ]

        regex_arr = [regex[x[0] + 1: x[1]] for x in new_split_indices]

        current_state, NFA = or_operator(regex_arr, NFA, current_state, start_state)
    else:
        brackets = get_brackets(regex)
        (current_outer_bracket, current_inner_brackets) = get_next_brackets(
            regex, brackets
        )
        while i < len(regex):
            # checking for alnum
            if bracket_type == "[":
                
                while regex.find("-") != -1:
                    index = regex.find("-")
                    if index == 0:
                        set_alnum_state(regex[0], NFA, current_state, current_state + 1)
                        regex = regex[index + 1:]
                        continue
                    elif index == len(regex) - 1:
                        set_alnum_state(regex[-1], NFA, current_state, current_state + 1)
                        regex = regex[:index]
                        continue
                    else:
                        char_before, char_after = regex[index - 1], regex[index + 1]
                        if ord(char_before) > ord(char_after):
                            raise Exception(
                                f"Invalid {char_before}-{char_after} range"
                            )
                        set_alnum_state(regex[index - 1: index + 2], NFA, current_state, current_state + 1)
                        regex = regex[:index - 1] + regex[index + 2:]
                for char in regex[i:]:
                    set_alnum_state(char, NFA, current_state, current_state + 1)
                current_state += 1
                break
            # checking for brackets
            elif current_outer_bracket and i == current_outer_bracket[0]:

                if (current_outer_bracket[1] + 1) < len(regex) and regex[
                    current_outer_bracket[1] + 1
                ] in regex_operators.keys():
                    current_state, new_NFA = regex_operators[
                        regex[current_outer_bracket[1] + 1]
                    ](
                        regex[i + 1: current_outer_bracket[1]],
                        NFA,
                        current_state,
                        bracket_type=regex[i],
                        regex_fn=get_regex,
                    )
                    i = current_outer_bracket[1] + 2
                else:
                    # we are at the start of the outer bracket
                    current_state, new_NFA = get_regex(
                        regex[i + 1: current_outer_bracket[1]],
                        NFA,
                        current_state,
                        True,
                        bracket_type=regex[i]
                    )
                    i = current_outer_bracket[1] + 1

                (current_outer_bracket, current_inner_brackets) = get_next_brackets(
                    regex, brackets
                )
            elif regex[i] == '\\' and bracket_type != "[":
                if i + 1 >= len(regex):
                    raise Exception("Escaped character found at end of regex/subregex")
                else:
                    char = regex[i+1]
                    if char in ESCAPED_CHARS:
                        set_alnum_state(char, NFA, current_state, current_state + 1)
                    else:
                        raise Exception(f"Invalid escaped character: \{char}")
                    current_state += 1
                    i += 2
            else:

                char = regex[i]
                if char in ESCAPED_CHARS:
                    raise Exception(f"Escape character is needed before {char}")

                if (i + 1) < len(regex) and regex[i + 1] in regex_operators.keys():
                    current_state, _ = regex_operators[regex[i + 1]](
                        char, NFA, current_state, regex_fn=get_regex
                    )
                    i += 1
                else:
                    set_alnum_state(char, NFA, current_state, current_state + 1)
                    if bracket_type == "(" or bracket_type is None:
                        current_state += 1

                i += 1

    return current_state, NFA


def zero_or_more(regex, NFA, current_state, bracket_type=None, regex_fn=get_regex):

    add_key_val(NFA, current_state, EPSILON, current_state + 1)
    current_state += 1
    start_state = current_state
    new_state, new_NFA = regex_fn(regex, NFA, start_state, bracket_type=bracket_type)

    add_key_val(NFA, start_state, EPSILON, new_state + 1)
    add_key_val(NFA, new_state, EPSILON, start_state)
    add_key_val(NFA, new_state, EPSILON, new_state + 1)
    NFA[new_state + 1] = dict()
    NFA = {**NFA, **new_NFA}
    return new_state + 1, NFA


def one_or_more(regex, NFA, current_state, bracket_type=None, regex_fn=get_regex):
    start_state = current_state
    new_state, new_NFA = regex_fn(regex, NFA, current_state, bracket_type=bracket_type)

    add_key_val(NFA, new_state, EPSILON, start_state)
    return new_state, NFA


def set_alnum_state(char, NFA, current_state, next_state):
    add_key_val(NFA, current_state, char, next_state)


def optional(regex, NFA, current_state, bracket_type=None, regex_fn=get_regex):
    start_state = current_state
    current_state, NFA = regex_fn(regex, NFA, current_state, bracket_type=bracket_type)
    add_key_val(NFA, start_state, EPSILON, current_state)
    return current_state, NFA


def or_operator(
    regex_arr, NFA, current_state, start_state, bracket_type=None, regex_fn=get_regex
):

    end_states = []
    for regex in regex_arr:
        current_state += 1
        add_key_val(NFA, start_state, EPSILON, current_state)
        current_state, NFA = regex_fn(
            regex, NFA, current_state, bracket_type=bracket_type
        )
        end_states.append(current_state)
    current_state += 1
    for end_state in end_states:
        add_key_val(NFA, end_state, EPSILON, current_state)

    return current_state, NFA


regex_operators = {"*": zero_or_more, "?": optional, "+": one_or_more}

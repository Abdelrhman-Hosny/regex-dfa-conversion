import json


def write_dfa_to_json(d, filename):
    with open(filename, "w") as f:
        json.dump(d, f)


def write_dict_to_json(d, filename):
    new_dict = {}
    for k1, v1 in d.items():
        if k1 == "startingState":
            new_dict[k1] = v1
            continue
        new_dict[k1] = {}
        for k2, v2 in v1.items():
            if k2 == "acceptingState":
                new_dict[k1][k2] = True
                continue
            new_dict[k1][k2] = []
            for state in v2:
                new_dict[k1][k2].append(state)
    with open(filename, "w") as f:
        json.dump(new_dict, f)


def read_json(filename):

    with open(filename, "r") as f:
        state_dict = json.load(f)
    return state_dict


def match_2_chars(regex, char1, char2):

    matches = []
    my_stack = []

    for i, c in enumerate(regex):
        if c == char1 and (i == 0 or regex[i - 1] != "\\"):
            my_stack.append(i)
        elif c == char2 and (i == 0 or regex[i - 1] != "\\"):
            if len(my_stack) == 0:
                raise Exception(f"Unmatched {char2}")
            matches.append((my_stack.pop(), i))
    if len(my_stack) > 0:
        raise Exception(f"Unmatched {char1}")
    return matches


def get_matched_parenthesis(regex):
    """
    Returns a list of tuples, each tuple has the start and end for each index
    """

    return match_2_chars(regex, "(", ")")


def get_matched_square_brackets(regex):
    """
    Returns a list of tuples, each tuple has the start and end for each index
    """
    return match_2_chars(regex, "[", "]")


def get_containing_brackets(brackets):
    """
    Returns a list, each element containts a tuple and a list
    The tuple contains the start and end index of the outermost bracket
    The list contains tuples of the indices of the innermost brackets

    inputs:
        brackets: a SORTED list of tuples including brackets
    """
    i = 0
    ret = []

    while i < len(brackets):
        s1, e1 = brackets[i]
        i += 1
        local_containing_brackets = []
        while i < len(brackets):
            s2, e2 = brackets[i]
            if s2 > s1 and e1 > e2:
                local_containing_brackets.append((s2, e2))
                i += 1
            else:
                break
        ret.append(((s1, e1), local_containing_brackets))
    return ret


def add_key_val(NFA, key1, key2, val):
    if not NFA.get(key1):
        NFA[key1] = {}
    if not NFA[key1].get(key2):
        NFA[key1][key2] = {val}
    NFA[key1][key2].add(val)

    return NFA


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


def get_next_brackets(regex, brackets):
    if not brackets:
        return None, None
    try:
        (outer_bracket, inner_brackets) = next(brackets)
        return remove_unnessasary_brackets(regex, outer_bracket, inner_brackets)
    except StopIteration:
        return None, None


def get_brackets(regex):

    brackets = get_matched_square_brackets(regex) + get_matched_parenthesis(regex)

    brackets = sorted(brackets, key=lambda x: x[0])

    return (x for x in get_containing_brackets(brackets))


def get_split_indices_for_or_operation(regex):

    brackets = list(get_brackets(regex))

    or_location = [i for i, c in enumerate(regex) if c == "|"]

    final_or_locations = []
    for or_index in or_location:
        temp = True
        for outer, _ in brackets:
            if outer[0] < or_index < outer[1]:
                temp = False
                break
        if temp:
            final_or_locations.append(or_index)

    return final_or_locations

import json


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


def validate_brackets(square_brackets, parenthesis):
    """
    Makes sure that brackets don't intersect
    e.g. ([)]
    """
    validate_square_brackets(square_brackets)
    brackets = square_brackets + parenthesis
    brackets = sorted(brackets, key=lambda x: x[0])

    intersecting_brackets = sum(
        [
            True if s1 < s2 < e1 and e1 < e2 else False
            for s1, e1 in brackets
            for s2, e2 in brackets
        ]
    )

    if intersecting_brackets != 0:
        raise Exception("Brackets intersect")


def validate_square_brackets(square_brackets):
    """
    Makes sure that brackets don't intersect
    [ab[cd]] not allowed
    """
    intersecting_brackets = sum(
        [
            True if s1 < s2 < e1 else False
            for s1, e1 in square_brackets
            for s2, e2 in square_brackets
        ]
    )

    if intersecting_brackets != 0:
        raise Exception("Square brackets intersect")


def validate_sorted_brackets(brackets):
    """
    Input is a sorted list of tuples containing bracket indices.
    Makes sure that brackets don't intersect
    e.g.    ([)] not allowed
            [()] allowed
    """
    intersecting_brackets = sum(
        [
            True if s1 < s2 < e1 and e1 < e2 else False
            for s1, e1 in brackets
            for s2, e2 in brackets
        ]
    )

    if intersecting_brackets != 0:
        raise Exception("Brackets intersect")


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
            regex = regex[:e2] + regex[e2 + 1 :]
            regex = regex[:s2] + regex[s2 + 1 :]
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
    validate_sorted_brackets(brackets)

    return (x for x in get_containing_brackets(brackets))


def detect_empty_nfa(NFA):
    if len(NFA) == 1:
        dict_keys = NFA.keys()
        val = NFA[list(dict_keys)[0]]
        if val == {}:
            return True
    return False


def get_num_of_last_state(NFA):
    return max([int(x[1:]) for x in NFA.keys()])


def detect_or_positions(regex):
    """
    Returns the bracket position of the ors
    [3, 9] means that there are two ors, one in the bracket that starts at index 3
    and another at bracket at index 9

    [-1 , 3] means that there is one outside of the brackets, and one at the bracket
    that starts at index 3
    """
    brackets = get_brackets(regex)
    or_indices = [i for i, c in enumerate(regex) if c == "|"]
    or_in_bracket = []
    for or_index in or_indices:
        belongs_to_bracket = -1
        for s, e in brackets:
            if s < or_index < e:
                belongs_to_bracket = s
                break
            or_in_bracket.append(belongs_to_bracket)
    return sorted(or_in_bracket)


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

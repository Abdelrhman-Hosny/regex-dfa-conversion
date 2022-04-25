import json


def write_dict_to_json(d, filename):
    with open(filename, "w") as f:
        json.dump(d, f)


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

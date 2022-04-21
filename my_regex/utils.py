import json


def write_dict_to_json(d, filename):
    with open(filename, "w") as f:
        json.dump(d, f)


def match_2_chars(regex, char1, char2):

    matches = []
    my_stack = []

    for i, c in enumerate(regex):
        if (c == char1 and (i == 0 or regex[i-1] != "\\")):
            my_stack.append(i)
        elif (c == char2 and (i == 0 or regex[i-1] != "\\")):
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

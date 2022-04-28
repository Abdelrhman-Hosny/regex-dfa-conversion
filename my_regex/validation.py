from my_regex.utils import get_matched_square_brackets, get_matched_parenthesis


class RegexValidator:
    def __init__(self, regex):
        self.regex = regex

        self.square_brackets = get_matched_square_brackets(regex)
        self.parenthesis = get_matched_parenthesis(regex)

        self.sorted_brackets = sorted(self.square_brackets + self.parenthesis, key=lambda x: x[0])

    def validate(self):
        validate_square_brackets(self.square_brackets)
        validate_sorted_brackets(self.sorted_brackets)


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

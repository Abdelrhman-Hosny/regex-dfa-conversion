from my_regex.utils import get_matched_square_brackets, get_matched_parenthesis


class RegexValidator:
    def __init__(self, regex):
        self.regex = regex

        self.square_brackets = get_matched_square_brackets(regex)
        self.parenthesis = get_matched_parenthesis(regex)
        self.sorted_brackets = sorted(self.square_brackets + self.parenthesis, key=lambda x: x[0])
        self.asterisk_indices = [i for i, char in enumerate(regex) if char == '*']
        self.plus_indices = [i for i, char in enumerate(regex) if char == '+']
        self.question_indices = [i for i, char in enumerate(regex) if char == '?']

    def validate(self):
        validate_square_brackets(self.square_brackets)
        validate_sorted_brackets(self.sorted_brackets)
        self.check_repeat_chars()

    def get_repeat_char_indices(self):
        return sorted(self.asterisk_indices + self.plus_indices + self.question_indices)

    def check_repeat_chars(self):
        repeat_char_indices = self.get_repeat_char_indices()
        if len(repeat_char_indices) < 2:
            return

        repeated_chars = [ repeat_char_indices[i] for i in range(len(repeat_char_indices) - 1)
                            if repeat_char_indices[i] + 1 == repeat_char_indices[i + 1]]
        
        if repeated_chars:
            # check if between square brackets
            for i in repeated_chars:
                in_brackets = False
                for bracket in self.square_brackets:
                    if bracket[0] < i < bracket[1]:
                        in_brackets = True
                        break
                if not in_brackets:
                    raise Exception("Invalid regex, repeated chars (+*?) cannot follow each other outside of square brackets")

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


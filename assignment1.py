# read input from command line
import sys
from my_regex.operators import construct_nfa
from my_regex.utils import write_dict_to_json
from my_regex.draw import draw_states
from my_regex.validation import RegexValidator

regex = sys.argv[-1]

if len(sys.argv) < 2:
    raise ValueError("Please provide a regex.")

validator = RegexValidator(regex)
validator.validate()

NFA = construct_nfa(regex)
write_dict_to_json(NFA, "nfa.json")
draw_states(NFA)
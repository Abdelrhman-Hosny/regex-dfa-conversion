import sys
from my_regex.operators import construct_nfa
from my_regex.utils import write_dict_to_json
from my_regex.draw import draw_states
from my_regex.validation import RegexValidator
from my_regex.conversion import convert_to_dfa
from my_regex.conversion_utils import write_dfa_to_json
from my_regex.minimization import minimize_dfa
from my_regex.draw import draw_states_dfa



if len(sys.argv) < 2:
    raise ValueError("Please provide a regex.")

regex = sys.argv[-1]

validator = RegexValidator(regex)
validator.validate()

# NFA part
NFA = construct_nfa(regex)
write_dict_to_json(NFA, "nfa.json")
draw_states(NFA)

# NFA -> DFA part
DFA, accepting_states_dfa = convert_to_dfa(NFA)
write_dfa_to_json(DFA, "dfa.json")
draw_states_dfa(DFA, accepting_states_dfa, "dfa")

# DFA -> DFA min part
minimized_DFA, accepting_states_dfa_min = minimize_dfa(DFA, accepting_states_dfa)
write_dfa_to_json(minimized_DFA, "dfa_min.json")
draw_states_dfa(minimized_DFA, accepting_states_dfa_min, "dfa_min")

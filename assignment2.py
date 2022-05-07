import sys
from my_regex.conversion import convert_to_dfa
from my_regex.conversion_utils import read_json, write_dfa_to_json
from my_regex.minimization import minimize_dfa
from my_regex.draw import draw_states_dfa

def change_keys_to_ints(states_dict):
    new_states_dict = {}
    for k, v in states_dict.items():
        if k != "startingState":
            new_states_dict[int(k)] = v
        else:
            new_states_dict[k] = v
    
    for k, v in new_states_dict.items():
        if k == "startingState": continue
        if "acceptingState" in v.keys():
            new_states_dict[k]["acceptingState"] = { True }
    return new_states_dict

if len(sys.argv) < 2:
    raise ValueError("Please provide an input filename")

if len(sys.argv) == 2:
    input_filename = sys.argv[1]
    output_filename = "dfa_min.json"
else:
    input_filename = sys.argv[-2]
    output_filename = sys.argv[-1]

NFA = read_json(input_filename)
DFA, accepting_states_dfa = convert_to_dfa(change_keys_to_ints(NFA))
minimized_DFA, accepting_states_dfa_min = minimize_dfa(DFA, accepting_states_dfa)

write_dfa_to_json(minimized_DFA, output_filename)
write_dfa_to_json(DFA, "dfa.json")

draw_states_dfa(DFA, accepting_states_dfa, "dfa")
draw_states_dfa(minimized_DFA, accepting_states_dfa_min, "dfa_min")
import json

def write_dict_to_json(d, filename):
    with open(filename, 'w') as f:
        json.dump(d, f)


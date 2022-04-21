from my_regex.utils import write_dict_to_json
reg = "abc"
play_dict = {
    "name": {
        "first": "Alice",
        "last": "Wonderland"
    },
    "description": "play a game",
    "usage": "play [game]"
}

write_dict_to_json(play_dict, "play.json")
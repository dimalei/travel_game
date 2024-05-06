import json

def list_to_json(data: list, filename:str):
    with open(filename, "w") as f:
        json.dump(data, f)
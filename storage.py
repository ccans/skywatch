import json

with open(r"storage.json", "r") as f:
    stored_json = json.load(f)

def get_stored_lat():
    return stored_json["lat"]

def get_stored_long():
    return stored_json["long"]

def store_data(lat, long):
    stored_json["lat"] = lat
    stored_json["long"] = long

    with open('storage.json', 'w') as json_file:
        json.dump(stored_json, json_file)

def get_stored_string():
    return stored_json["stored_string"]

def get_planets_arr():
    return stored_json["planets_arr"]
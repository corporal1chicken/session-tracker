from constants import SAVE_PATH
import json

def save_data(groups):
    print(groups)
    try:
        with open(SAVE_PATH, "w") as file:
            json.dump(groups, file)
    except Exception as error:
        print(f"An error occured whilst saving: {error}")

def load_data():
    saved_groups = {}

    try:
        with open(SAVE_PATH, 'r') as file:
            saved_groups = json.load(file)
        
    except FileNotFoundError:
        print("File wasn't found")
    except json.JSONDecodeError:
        print("File is empty")

    return saved_groups

def get_valid_groups(groups):
    valid_groups = {}

    for name, data in groups.items():
        if len(data['items']) == 0: continue
        if not data['active']: continue

        valid_groups[name] = data

    if len(valid_groups) == 0:
        return False, "No valid groups", {}

    return True, "Success", valid_groups
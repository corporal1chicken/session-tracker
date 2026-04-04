from constants import SAVE_PATH
import json

def save_data(groups):
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
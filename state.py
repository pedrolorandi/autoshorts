import json

STATE_FILE = 'state.json'

def save_state(data):
    with open(STATE_FILE, 'w') as file:
        json.dump(data, file)

def load_state():
    try:
        with open(STATE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def clear_state():
    with open(STATE_FILE, 'w') as file:
        json.dump({}, file)
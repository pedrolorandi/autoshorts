import json

STATE_FILE = 'state.json'

def save_state(data):
  # Save the state to a file
  with open(STATE_FILE, 'w') as file:
    json.dump(data, file)

def load_state():
  # Load the state from a file, return empty dict if file not found
  try:
    with open(STATE_FILE, 'r') as file:
      return json.load(file)
  except FileNotFoundError:
    return {}

def clear_state():
  # Clear the state by writing an empty dict to the file
  with open(STATE_FILE, 'w') as file:
    json.dump({}, file)

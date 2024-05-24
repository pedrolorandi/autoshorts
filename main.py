from helper import clear_and_wait
from scraper import get_horoscope
from script_creator import create_script
from state import load_state, save_state, clear_state
  
# Run the scraper
def main():
  state = load_state()
  clear_state()

  # Scrape horoscope and save the state
  horoscope = get_horoscope()
  state['horoscope'] = horoscope
  save_state(state)

  # Create script and save the state
  script = create_script(state['horoscope'])
  state['scripts'] = script
  save_state(state)

if __name__ == '__main__':
  main()
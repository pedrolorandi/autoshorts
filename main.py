from helper import clear_and_wait
from state import load_state, save_state, clear_state
from scraper import get_horoscope
from script_creator import create_script
from phrase_creator import create_phrases
from audio_creator import create_audio
from image_creator import create_image
  
# Run the scraper
def main():
  try:
    state = load_state()
    # clear_state()

    # # Scrape horoscope and save the state
    # horoscope = get_horoscope()
    # state['horoscope'] = horoscope
    # save_state(state)

    # # Create script and save the state
    # script = create_script(state['horoscope'])
    # state['scripts'] = script
    # save_state(state)

    # # Create phrases and save the state
    # phrases = create_phrases(state['scripts'])
    # state['phrases'] = phrases
    # save_state(state)

    # Create audio
    # create_audio(state['phrases'])

    # Create image
    create_image(state['phrases'])

  except Exception as e:
    print(f"An error occurred: {e}")

if __name__ == '__main__':
  main()
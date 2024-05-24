import os
import openai
from helper import zodiac_signs, clear_and_wait

openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def create_image(phrases):
  clear_and_wait()  # Clear console or perform any necessary setup

  # Verify if folder 'audio' exists, if not, create it
  image_folder = 'image'
  if not os.path.exists(image_folder):
    os.makedirs(image_folder)

  for sign_name in zodiac_signs:
    phrases_number = len(phrases[sign_name]['phrases'])

    for i, phrase in enumerate(phrases[sign_name]['phrases']):
      print(f"Creating image for {sign_name} ({i + 1}/{phrases_number})")
      # Create image here

  clear_and_wait()  # Clear console or perform any necessary cleanup
  return True
import os
import openai
from dotenv import load_dotenv
from helper import zodiac_signs, clear_and_wait

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_script(horoscope):
  clear_and_wait()  # Clear console or perform any necessary setup
  scripts = {}

  for sign_name in zodiac_signs:
    try:
      print(f"Creating script for {sign_name}")
      response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
          {"role": "system", "content": "You are a professional astrologer. The user will send you some information and your job is to rewrite it in a more professional manner. The script should contain 120-200 words."},
          {"role": "user", "content": horoscope[sign_name]['text']}
        ]
      )
      scripts[sign_name] = {'script': response.choices[0].message['content']}
    except Exception as e:
      print(f"An error occurred while creating script for {sign_name}: {e}")
      scripts[sign_name] = {'script': ''}

  clear_and_wait()  # Clear console or perform any necessary cleanup
  return scripts

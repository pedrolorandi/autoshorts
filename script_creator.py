import os
import openai
from helper import zodiac_signs, clear_and_wait

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_script(horoscope):
  clear_and_wait()  # Clear console or perform any necessary setup
  scripts = {}

  for sign_name in zodiac_signs:
    try:
      print(f"Creating script for {sign_name}")
      response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
          {"role": "system", "content": "You are a professional astrologer. The user will send you some information and your job is to rewrite it in a more professional manner. The script should contain 120 words. CREATE SENTENCES WITH 6 to 8 WORDS ONLY. MAKE SURE TO USE SIMPLE WORDS IN A CLEVER WAY. MAKE THE SCRIPT EASY TO UNDERSTAND. DO NOT ADD ANY NEW INFORMATION. DO NOT ADD NEW LINES. DO NOT ADD SIGNATURES. DO NOT ADD ANY TYPE OF QUOTES. DO NOT ADD SPECIAL CHARACTERS. DO NOT ADD EMOJI."},
          {"role": "user", "content": horoscope[sign_name]['text']}
        ]
      )
      # Decode the script text to handle any Unicode issues
      script_text = response.choices[0].message['content']
      scripts[sign_name] = {'script': script_text}
    except Exception as e:
      print(f"An error occurred while creating script for {sign_name}: {e}")
      scripts[sign_name] = {'script': ''}

  clear_and_wait()  # Clear console or perform any necessary cleanup
  return scripts

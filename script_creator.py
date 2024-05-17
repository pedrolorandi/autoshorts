import os
import openai
from dotenv import load_dotenv
from helper import zodiac_signs, clear_and_wait

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_script(horoscope):
    clear_and_wait()

    scripts = {}

    for sign_name in zodiac_signs:
        print(f"Creating script for {sign_name}")
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional astrologer. The user will send you some information and your job is to rewrite it in a more professional manner. The script should contain 120-200 words."},
                {"role": "user", "content": horoscope[sign_name]['text']}
            ]
        )

        script = scripts[sign_name] = response.choices[0].message['content']

    clear_and_wait()
    return scripts

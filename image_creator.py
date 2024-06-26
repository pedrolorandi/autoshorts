import os
import openai
from dotenv import load_dotenv
from helper import zodiac_signs, clear_and_wait

import base64
from PIL import Image
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_current_moon_phase():
  """
  Get the current moon phase using the OpenAI API.
  """
  try:
    print("Getting the current moon phase")
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-0125",
      messages=[
        {"role": "system", "content": "You are an assistant. The user will ask you for the current moon phase. RETURN THE MOON PHASE ONLY. DO NOT ADD ANY ADDITIONAL INFORMATION. DO NOT ADD ANY NEW LINES. DO NOT ADD SIGNATURES. DO NOT ADD ANY TYPE OF QUOTES. DO NOT ADD SPECIAL CHARACTERS. DO NOT ADD EMOJI."},
        {"role": "user", "content": "What is the current moon phase?"}
      ]
    )
    # Decode the script text to handle any Unicode issues
    print(response.choices[0].message['content'])
  except Exception as e:
    print(f"An error occurred while getting the moon phase: {e}")
  return None

def create_image(phrases):
  clear_and_wait()  # Clear console or perform any necessary setup

  # Verify if folder 'audio' exists, if not, create it
  image_folder = 'image'
  if not os.path.exists(image_folder):
    os.makedirs(image_folder)

  # Iterate through each zodiac sign and their corresponding phrases
  for sign_name in zodiac_signs:
    phrases_number = len(phrases[sign_name]['phrases'])

    # Generate images for each phrase
    for i, phrase in enumerate(phrases[sign_name]['phrases']):
      try:
        print(f"Creating image for {sign_name} ({i + 1}/{phrases_number})")

        prompt = f"DO NOT INCLUDE TEXT OR PARAGRAPHS OF ANY KIND. DO NOT CREATE DIAGRAMS. Create ONE image only for this phrase: '{phrase}' in the highest resolution. The style of the images should be a blend of surrealism and fantasy with elements of digital art. Use atmospheric lighting to create a sense of calm and introspection. Make the image towared the female public. DO NOT INCLUDE TEXT OR PARAGRAPHS OF ANY KIND."

        if i == 0:
          prompt = "CREATE A VERY INTRIGUING AND CAPTIVATING IMAGE THAT MAKES THE VIEWER STOP SCROLLING IMMEDIATELY. MAKE IT SAFE FOR WORK. " + prompt

        response = openai.Image.create(
          model="dall-e-3",
          prompt=prompt,
          size="1024x1024",
          quality="standard",
          response_format="b64_json",
          style="vivid",
          n=1,
        )

        # Decode the base64 image data
        base64_image = response['data'][0]['b64_json']
        decoded_image = base64.b64decode(base64_image)

        # Open the image using PIL
        image = Image.open(BytesIO(decoded_image))

        # Save the image to the specified folder
        image.save(f"{image_folder}/{sign_name}_{i}.jpg")

      except Exception as e:
        print(f"Error creating image for {sign_name} ({i + 1}/{phrases_number}): {e}")
        os.system('sleep 60')

  clear_and_wait()  # Clear console or perform any necessary cleanup
  return True
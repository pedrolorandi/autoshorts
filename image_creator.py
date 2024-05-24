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
        response = openai.Image.create(
          model="dall-e-3",
          prompt=f"Do not include any text in the image. Create an image for this phrase: '{phrase}' in the highest resolution. The style of the images should be a blend of surrealism and fantasy with elements of digital art. The image should feature a serene and reflective scene with surreal elements. The landscape should have an ethereal quality with vibrant colors and detailed composition. Use atmospheric lighting to create a sense of calm and introspection, incorporating symbolism to convey themes of self-assessment, progress, and personal growth.",
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
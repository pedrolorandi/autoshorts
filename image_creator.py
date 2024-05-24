import os
import openai
from dotenv import load_dotenv
from helper import zodiac_signs, clear_and_wait

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_image(phrases):
  clear_and_wait()  # Clear console or perform any necessary setup

  # Verify if folder 'audio' exists, if not, create it
  image_folder = 'image'
  if not os.path.exists(image_folder):
    os.makedirs(image_folder)

  for sign_name in zodiac_signs:
    phrases_number = len(phrases[sign_name]['phrases'])

    for i, phrase in enumerate(phrases[sign_name]['phrases']):
      try:
        print(f"Creating image for {sign_name} ({i + 1}/{phrases_number})")
        response = openai.Image.create(
          model="dall-e-3",
          # prompt=f"Do not include any text in the image. Create an image for this phrase: '{phrase}' in the highest resolution. The style of the images should be a blend of surrealism and fantasy with elements of digital art. The image should feature a serene and reflective scene with surreal elements. The landscape should have an ethereal quality with vibrant colors and detailed composition. Use atmospheric lighting to create a sense of calm and introspection, incorporating symbolism to convey themes of self-assessment, progress, and personal growth.",
          prompt=f"Do not include any text in the image. Create an image for this phrase: '{phrase}' in the highest resolution.",
          size="1024x1024",
          quality="standard",
          n=1,
        )

        image_url = response['data'][0]['url']
        print(image_url)

      except Exception as e:
        print(f"Error creating image for {sign_name} ({i + 1}/{phrases_number}): {e}")
        os.system('sleep 60')

  clear_and_wait()  # Clear console or perform any necessary cleanup
  return True
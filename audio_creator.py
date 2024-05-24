import os
from elevenlabs import Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
from helper import zodiac_signs, clear_and_wait

def create_audio(phrases):
  clear_and_wait()  # Clear console or perform any necessary setup

  client = ElevenLabs(
    api_key=os.getenv('ELEVEN_API_KEY')
  )

  # Verify if folder 'audio' exists, if not, create it
  audio_folder = 'audio'
  if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

  for sign_name in zodiac_signs:
    phrases_number = len(phrases[sign_name]['phrases'])

    for i, phrase in enumerate(phrases[sign_name]['phrases']):
      print(f"Creating audio for {sign_name} ({i + 1}/{phrases_number})")
      audio = client.generate(
        text=phrase,
        voice=Voice(voice_id='24C3xoIzMQGcoH3tAbyB'),
        model="eleven_multilingual_v2",
      )

      # Save the audio file in WAV format
      with open(f'audio/{sign_name}_{i}.wav', 'wb') as f:
        f.write(audio)

  clear_and_wait()  # Clear console or perform any necessary cleanup
  return True   
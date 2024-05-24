import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save, Voice, VoiceSettings
from helper import zodiac_signs, clear_and_wait

def create_audio(phrases):
  clear_and_wait()  # Clear console or perform any necessary setup

  try:
    client = ElevenLabs(
      api_key=os.getenv('ELEVEN_API_KEY')
    )

    # Verify if folder 'audio' exists, if not, create it
    audio_folder = 'audio'
    if not os.path.exists(audio_folder):
      os.makedirs(audio_folder)

  except Exception as e:
    print(f"Error initializing ElevenLabs client: {e}")
    return False

  for sign_name in zodiac_signs:
    phrases_number = len(phrases[sign_name]['phrases'])

    for i, phrase in enumerate(phrases[sign_name]['phrases']):
      try:
        print(f"Creating audio for {sign_name} ({i + 1}/{phrases_number})")
        audio = client.generate(
          text=phrase.strip(),
          voice=Voice(
            voice_id='gj8rBFVprjSvDpHXxlro',
            settings=VoiceSettings(stability=0.4, similarity_boost=0.7, style=0.0, use_speaker_boost=False),
          ),
          model="eleven_multilingual_v2",
        )

        # Save the audio file in WAV format
        save(audio, f"{audio_folder}/{sign_name}_{i}.wav")

      except Exception as e:
        print(f"Error creating audio for {sign_name} ({i + 1}/{phrases_number}): {e}")

  clear_and_wait()  # Clear console or perform any necessary cleanup
  return True

from helper import zodiac_signs, clear_and_wait

def create_phrases(scripts):
  clear_and_wait()  # Clear console or perform any necessary setup
  phrases = {}

  for sign_name in zodiac_signs:
    print(f"Creating phrase for {sign_name}")

    # Check if the script exists for the zodiac sign
    if sign_name not in scripts or 'script' not in scripts[sign_name]:
      phrases[sign_name] = {'phrases': []}
    else:
      script = scripts[sign_name]['script']
      # Split the script into phrases after each punctuation and strip whitespace
      phrases[sign_name] = {'phrases': [phrase.strip() for phrase in script.split('. ') if phrase.strip()]}

  return phrases

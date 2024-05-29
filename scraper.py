import requests
from helper import zodiac_signs, clear_and_wait
from bs4 import BeautifulSoup

def get_horoscope_from_source1():
  horoscope = {}

  # Source 01 => Horoscope.com
  base_url = 'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign='

  for sign_id in range(0, len(zodiac_signs)):
    sign_name = zodiac_signs[sign_id]

    try:
      print(f"Scraping {sign_name} from Horoscope.com")
      response = requests.get(f"{base_url}{sign_id + 1}")
      response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
      soup = BeautifulSoup(response.content, 'html.parser')

      # Extract the horoscope text
      full_text = soup.find('div', class_='content').find_next('p').text.strip()
      horoscope_text = full_text.split(' - ', 1)[1].strip()

      # Store the horoscope text in a dictionary
      horoscope[sign_name] = horoscope_text
    except Exception as e:
      print(f"An error occurred while scraping {sign_name} from Horoscope.com: {e}")
      horoscope[sign_name] = ''

  return horoscope

def get_horoscope_from_source2():
  horoscope = {}

  # Source 02 => Astrostyle.com
  base_url = 'https://astrostyle.com/horoscopes/daily/'

  for sign_name in zodiac_signs:
    try:
      print(f"Scraping {sign_name} from Astrostyle.com")
      response = requests.get(f"{base_url}{sign_name.lower()}/")
      response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
      soup = BeautifulSoup(response.content, 'html.parser')

      # Extract the horoscope text
      horoscope_text = soup.find('div', class_='horoscope-content', style="display:block;").find_next('p').text.strip()

      # Store the horoscope text in a dictionary
      horoscope[sign_name] = horoscope_text
    except Exception as e:
      print(f"An error occurred while scraping {sign_name} from Astrostyle.com: {e}")
      horoscope[sign_name] = ''

  return horoscope

def get_horoscope():
  clear_and_wait()  # Clear console or perform any necessary setup
  horoscope_source1 = get_horoscope_from_source1()
  horoscope_source2 = get_horoscope_from_source2()

  horoscope = {}

  for sign_name in zodiac_signs:
    # Combine texts from both sources
    horoscope[sign_name] = {
      'text': horoscope_source1[sign_name] + " " + horoscope_source2[sign_name],
    }

  clear_and_wait()  # Clear console or perform any necessary cleanup
  return horoscope

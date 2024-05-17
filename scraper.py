# Scrape horoscope from pages and return the horoscope text for each zodiac sign

import requests
from bs4 import BeautifulSoup

# List of zodiac signs in order corresponding to the sign_id
zodiac_signs = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

def get_horoscope_from_souce1():
  horoscope = {}

  # Source 01 => Horoscope.com
  base_url = 'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign='

  for sign_id in range(1, 13):
    response = requests.get(f"{base_url}{sign_id}")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the horoscope text
    full_text = soup.find('div', class_='content').find_next('p').text.strip()
    horoscope_text = full_text.split(' - ', 1)[1].strip()

    # Store the horoscope text in a dictionary
    sign_name = zodiac_signs[sign_id - 1]
    horoscope[sign_name] = horoscope_text
  return horoscope

def get_horoscope():
  horoscope_source1 = get_horoscope_from_souce1()
  print(horoscope_source1)

  # horoscope = {}

  # for sign in zodiac_signs:
  #   horoscope[sign] = {
  #     text: horoscope_source1[sign]
  #   }

  # return horoscope
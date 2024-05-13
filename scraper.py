# Scrape Amazon's information page for a product

import requests
from bs4 import BeautifulSoup

def fetch_product_details(url):

  # Add a header to mimic a real user request
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  }

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup.prettify()
from scraper import fetch_product_details
  
# URL of the page to scrape
url = 'https://www.amazon.ca/Ashwagandha-Absorption-Resistant-Increases-Enhancement/dp/B09V3C98LC'

# Run the scraper
def main():
  soup = fetch_product_details(url)
  print(soup)

if __name__ == '__main__':
  main()
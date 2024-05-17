from scraper import get_horoscope
  
# Run the scraper
def main():
  horoscope = get_horoscope()
  print(horoscope)

if __name__ == '__main__':
  main()
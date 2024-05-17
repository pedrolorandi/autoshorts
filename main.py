from helper import clear_and_wait
from scraper import get_horoscope
  
# Run the scraper
def main():
  clear_and_wait()
  horoscope = get_horoscope()
  print(horoscope)

if __name__ == '__main__':
  main()
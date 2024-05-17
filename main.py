from helper import clear_and_wait
from scraper import get_horoscope
from script_creator import create_script
  
# Run the scraper
def main():
  horoscope = get_horoscope()
  # print(horoscope)
  script = create_script(horoscope)
  print(script)

if __name__ == '__main__':
  main()
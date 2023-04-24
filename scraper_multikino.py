from contextlib import contextmanager
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime


# Constants
CHROMEDRIVER_PATH = '/path/to/chromedriver'
URL_FORMAT = 'https://multikino.pl/repertuar/{}/teraz-gramy?data={}'
WAIT_TIME = 10

# Format daty w postaci DD-MM-YYYY
showing_date = datetime.today().strftime('%d-%m-%Y')
city = "kielce"


@contextmanager
def get_chrome_driver():
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # run Chrome in headless mode
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        yield driver
    finally:
        driver.quit()


def get_movie_titles(city, showing_date):
    """
    This function uses Selenium and BeautifulSoup to scrape the Multikino website
    and get a list of movie titles that are currently playing in the given city
    on the specified showing date.

    Args:
        city (str): The name of the city where the cinema is located.
        showing_date (str): The date in format DD-MM-YYYY for which movie titles are to be retrieved.

    Returns:
        A list of movie titles that are currently playing in the specified city on the specified date.
    """
    try:
        # Navigate to the page
        url = URL_FORMAT.format(city, showing_date)
        with get_chrome_driver() as driver:
            driver.get(url)

            # Wait for the page to load
            wait = WebDriverWait(driver, WAIT_TIME)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'filmlist__item')))

            # Get the page source and parse it with BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find the film list
            film_list = soup.find('div', {'class': 'filmlist container container-small expand-small'})

            # Find the film items and get the titles
            film_items = film_list.find_all('div', {'class': 'filmlist__item'})
            titles = [item.
                      find('div', {'class': 'filmlist__info-txt'}).
                      find('span', {'data-v-9364a27e': True}).
                      text for item in film_items]

            return titles

    except (WebDriverException, AttributeError) as e:
        print(f"Error occurred: {str(e)}")
        return []


titles = get_movie_titles(city, showing_date)
print(titles)

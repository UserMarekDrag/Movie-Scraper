import json
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
WAIT_TIME = 30

# Date format in the form of YYYY-MM-DD
showing_date = datetime.today().strftime('%Y-%m-%d')
city = "kielce"

@contextmanager
def get_chrome_driver():
    """
    This context manager creates a headless Chrome WebDriver instance,
    manages its lifecycle, and cleans up after it is done.
    """
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # run Chrome in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        yield driver
    finally:
        driver.quit()


def get_movie_info(city, showing_date):
    """
    This function uses Selenium and BeautifulSoup to scrape the Multikino website
    and get information about movies that are currently playing in the given city
    on the specified showing date.

    Args:
        city (str): The name of the city where the cinema is located.
        showing_date (str): The date in format DD-MM-YYYY for which movie information is to be retrieved.

    Returns:
        A list of dictionaries, where each dictionary represents information about a single movie.
        Each dictionary has the following keys:
        - title (str): The title of the movie.
        - description (str): The description of the movie.
        - hour (str): The time when the movie is playing.
        - booking_link (str): The link for booking the movie.
    """
    try:
        url = URL_FORMAT.format(city, showing_date)
        with get_chrome_driver() as driver:
            driver.get(url)

            wait = WebDriverWait(driver, WAIT_TIME)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'filmlist__item')))

            film_items = driver.find_elements(By.CLASS_NAME, 'filmlist__item')
            movie_info_list = []

            for item in film_items:
                driver.execute_script("arguments[0].scrollIntoView();", item)

                # now you have to parse the item's HTML with BeautifulSoup
                item_html = item.get_attribute('outerHTML')
                soup_item = BeautifulSoup(item_html, 'html.parser')

                # Continue the process here using 'soup_item' instead of 'item'
                title = soup_item.find('div', {'class': 'filmlist__info-txt'}).find('span',
                                                                                    {'data-v-9364a27e': True}).text

                category = soup_item.find('a', {
                    'class': 'film-details__item',
                    'rv-class-film-details__item--selected': 'genre.highlighted'
                }).text.strip() if soup_item.find('a', {
                    'class': 'film-details__item',
                    'rv-class-film-details__item--selected': 'genre.highlighted'
                }) else ''

                description = soup_item.\
                    find('p', {'class': 'filmlist__synopsis--twoLines'}).text if soup_item.\
                    find('p', {'class': 'filmlist__synopsis--twoLines'}) else 'No description'

                # Get the image URL
                img_url = soup_item.find('img').get('src')

                show_info = [{
                    'hour': time.find('time', {'class': 'default'}).text.strip(),
                    'booking_link': 'https://multikino.pl' + time.find('a')['href']
                } for time in soup_item.find_all('li', {'class': 'times__detail'})
                    if time.find('time', {'class': 'default'}) is not None]

                # Append the extracted info to movie_info_list
                movie_info_list.append({
                    'title': title,
                    'category': category,
                    'description': description,
                    'image': img_url,
                    'show_info': show_info
                })

    except (WebDriverException, AttributeError) as e:
        print(f"Error occurred: {str(e)}")

    return movie_info_list


movie_info_list = get_movie_info(city, showing_date)
print(json.dumps(movie_info_list, indent=4, ensure_ascii=False))

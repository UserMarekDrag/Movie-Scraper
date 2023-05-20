import json
from contextlib import contextmanager
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup

# Constants
CHROMEDRIVER_PATH = '/path/to/chromedriver'
URL_FORMAT = 'https://www.helios.pl/{},{}/Repertuar/index/dzien/{}/kino/{}'
WAIT_TIME = 10

day = 1
city = "kielce"
cinema_numb = 13
movie_info_list = []


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


def get_movie_info(city, day, cinema_numb):
    """
    This function uses Selenium and BeautifulSoup to scrape the Helio website
    and get information about movies that are currently playing in the given city
    on the specified showing date.

    Args:
        city (str): The name of the city where the cinema is located.
        day (int): The date where 0 == today, 1 == tomorrow, ....
        cinema_numb (int): The number of the cinema, number is unique.

    Returns:
        A list of dictionaries, where each dictionary represents information about a single movie.
        Each dictionary has the following keys:
        - title (str): The title of the movie.
        - hour (str): The time when the movie is playing.
        - booking_link (str): The link for booking the movie.
    """
    try:
        url = URL_FORMAT.format(cinema_numb, city, day, cinema_numb)
        with get_chrome_driver() as driver:
            driver.get(url)

            wait = WebDriverWait(driver, WAIT_TIME)
            wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'seances-list')))

            film_items = driver.find_elements(By.XPATH, "//ul/*[contains(@class, 'seance gallery-column')]")

            for item in film_items:
                driver.execute_script("arguments[0].scrollIntoView();", item)

                # now you have to parse the item's HTML with BeautifulSoup
                item_html = item.get_attribute('outerHTML')
                soup_item = BeautifulSoup(item_html, 'html.parser')

                # Continue the process here using 'soup_item' instead of 'item'
                title = soup_item.find('h2', {'class': 'movie-title'}).find('a', {'class': 'movie-link'}).text.strip()

                show_info = [{
                    'hour': time.find('a', {'class': 'hour-link fancybox-reservation'}).text.strip(),
                    'booking_link': 'https://helios.pl' + time.find('a')['href']
                } for time in soup_item.find_all('li', {'class': 'hour toolTipContainer'})
                    if time.find('a', {'class': 'hour-link fancybox-reservation'}) is not None]

                # Append the extracted info to movie_info_list
                movie_info_list.append({
                    'title': title,
                    'show_info': show_info
                })

    except (WebDriverException, AttributeError) as e:
        print(f"Error occurred: {str(e)}")

    return movie_info_list


movie_info = get_movie_info(city, day, cinema_numb)
print(json.dumps(movie_info, indent=4, ensure_ascii=False))

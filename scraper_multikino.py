from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_movie_titles(city, showing_date):
    # Setup Selenium web driver
    service = Service('path/to/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # run Chrome in headless mode
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the page
    url = f'https://multikino.pl/repertuar/{city}/teraz-gramy?data={showing_date}'
    driver.get(url)

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
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

    # Quit the driver and return the titles
    driver.quit()
    return titles


kielce_24_04_multikino = get_movie_titles("kielce", "25-04-2023")
print(kielce_24_04_multikino)

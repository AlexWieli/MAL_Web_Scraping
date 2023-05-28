from urllib.parse import quote
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Firefox options
options = Options()
options.headless = False  # Headless mode toggle

# Path to Geckodriver executable
geckodriver_path = '/opt/homebrew/bin/geckodriver'

# Initialize Firefox driver
driver = webdriver.Firefox(service=Service(geckodriver_path), options=options)

################################################################################
# This part prepares links to current top anime
################################################################################

base_url = 'https://myanimelist.net/'
driver.get(base_url)

top_url = driver.find_element(By.CLASS_NAME, 'footer-ranking').find_element(By.TAG_NAME, 'a').get_attribute('href')
driver.get(top_url)

anime_links = []

def scrape_links(url):
    driver.get(url)
    tags = driver.find_elements(By.CLASS_NAME, 'hoverinfo_trigger')
    links = [tag.get_attribute('href') for tag in tags if tag.get_attribute('href') is not None]
    return links

anime_links.extend(scrape_links(top_url))

# Manual limit - increments of 50 are checked
link_limit = 100

while len(anime_links) < link_limit:
    next_button = driver.find_element(By.CLASS_NAME, 'link-blue-box.next')
    if next_button:
        next_page_link = next_button.get_attribute('href')
        anime_links.extend(scrape_links(next_page_link))
    else:
        break

for link in anime_links:
    print(link)
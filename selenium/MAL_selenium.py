from urllib.parse import quote
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

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
link_limit = 50

while len(anime_links) < link_limit:
    next_button = driver.find_element(By.CLASS_NAME, 'link-blue-box.next')
    if next_button:
        next_page_link = next_button.get_attribute('href')
        anime_links.extend(scrape_links(next_page_link))
    else:
        break

for link in anime_links:
    print(link)

################################################################################
# This part scrapes anime data
################################################################################

d = pd.DataFrame(
    {'title': [], 'type': [], 'episodes': [], 'status': [], 'aired': [], 'studios': [], 'source': [], 'genres': [],
     'theme': [], 'demo': [], 'duration': [], 'rating': [], 'score': [], 'ranked': [], 'popularity': [], 'members': [],
     'fav': []})

def scrape_data(element):
    time.sleep(0.4)
    return element.text.strip() if element else ''

for link in anime_links:
    url = quote(link, safe=':/')
    driver.get(url)

    time.sleep(0.4) # adjust the waiting time accordingly

    title = scrape_data(driver.find_element(By.XPATH, "//h1[@class='title-name h1_bold_none']"))
    type = scrape_data(driver.find_element(By.XPATH, "//span[text()='Type:']/following-sibling::a"))
    episodes = scrape_data(driver.find_element(By.XPATH, "//span[text()='Episodes:']/parent::*"))
    episodes = episodes.replace('Episodes: ', '')
    status = scrape_data(driver.find_element(By.XPATH, "//span[text()='Status:']/parent::*"))
    status = status.replace('Status: ', '')
    aired = scrape_data(driver.find_element(By.XPATH, "//span[text()='Aired:']/parent::*"))
    aired = aired.replace('Aired: ', '')
    studios = scrape_data(driver.find_element(By.XPATH, "//span[text()='Studios:']/parent::*"))
    studios = studios.replace('Studios: ', '')
    source = scrape_data(driver.find_element(By.XPATH, "//span[text()='Source:']/parent::*"))
    source = source.replace('Source: ', '')
    genres = ', '.join(a.text.strip() for a in driver.find_elements(By.XPATH, "//span[contains(text(), 'Genre') or contains(text(), 'Genres')]/parent::*/a"))
    themes = ', '.join(a.text.strip() for a in driver.find_elements(By.XPATH, "//span[contains(text(), 'Theme') or contains(text(), 'Themes')]/parent::*/a"))
    demo = ', '.join(a.text.strip() for a in driver.find_elements(By.XPATH, "//span[text()='Demographic:']/parent::*/a"))
    duration = scrape_data(driver.find_element(By.XPATH, "//span[text()='Duration:']/parent::*"))
    duration = duration.replace('Duration: ', '')
    rating = scrape_data(driver.find_element(By.XPATH, "//span[text()='Rating:']/parent::*"))
    rating = rating.replace('Rating: ', '')
    score = scrape_data(driver.find_element(By.XPATH, "//span[text()='Score:']/following-sibling::span"))
    ranked = re.search(r'#(\d+)', scrape_data(driver.find_element(By.XPATH, "//span[text()='Ranked:']/parent::*")))
    ranked = ranked.group(1)[:-2] if ranked else ''
    popularity = re.search(r'#(\d+)', scrape_data(driver.find_element(By.XPATH, "//span[text()='Popularity:']/parent::*")))
    popularity = popularity.group(1) if popularity else ''
    members = scrape_data(driver.find_element(By.XPATH, "//span[text()='Members:']/parent::*"))
    members = members.replace('Members: ', '')
    fav = scrape_data(driver.find_element(By.XPATH, "//span[text()='Favorites:']/parent::*"))
    fav = fav.replace('Favorites: ', '')

    anime = {'title': title, 'type': type, 'episodes': episodes, 'status': status, 'aired': aired, 'studios': studios,
             'source': source, 'genres': genres, 'theme': themes, 'demo': demo, 'duration': duration, 'rating': rating,
             'score': score, 'ranked': ranked, 'popularity': popularity, 'members': members, 'fav': fav}
    d = pd.concat([d, pd.DataFrame(anime, index=[0])], ignore_index=True)

driver.quit()

print(d)
d.to_csv('anime_Selenium.csv')
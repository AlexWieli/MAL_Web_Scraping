################################################################################
# Scraping Project - My Anime List | Aleksander Wieliński 420272 & Jakub Gazda 419272
################################################################################

from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd

################################################################################
# This part prepares links to current top anime
################################################################################

base_url = 'https://myanimelist.net/'
html = request.urlopen(base_url)
bs = BS(html.read(), 'html.parser')

top_url = bs.find('div', {'class': 'footer-ranking'}).div.div.h3.a['href']
html = request.urlopen(top_url)
bs = BS(html.read(), 'html.parser')

anime_links = []

def scrape_links(url):
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')
    tags = bs.find_all(class_='hoverinfo_trigger fl-l ml12 mr8')
    links = [tag['href'] for tag in tags]
    return links

anime_links.extend(scrape_links(top_url))

while True:
    next_page_link = None
    next_button = bs.find(class_='link-blue-box next')
    if next_button:
        next_page_link = top_url + next_button['href']
        anime_links.extend(scrape_links(next_page_link))
    else:
        break
    html = request.urlopen(next_page_link)
    bs = BS(html.read(), 'html.parser')

for link in anime_links:
    print(link)

################################################################################
# This part scraps painters
################################################################################
d = pd.DataFrame({'name':[], 'birth':[], 'death':[], 'nationality':[]})

for painter_link in painter_links[:100]:
    print(painter_link)

    html = request.urlopen(painter_link)
    bs = BS(html.read(), 'html.parser')
    
    try:
        name = bs.find('h1').text
    except:
        name = ''
    
    try:
        birth = bs.find('th',string = 'Born').next_sibling.text
        birth = re.findall('[0-9]+\s+[A-Za-z]+\s+[0-9]+', birth)[0]
    except:
        birth = ''
    
    try:
        death = bs.find('th',string = 'Died').next_sibling.text
        death = re.findall('[0-9]+\s+[A-Za-z]+\s+[0-9]+', death)[0]
    except:
        death = ''
    
    try:
        nationality = bs.find('th',string = 'Nationality').next_sibling.text
    except:
        nationality = ''
    
    painter = {'name':name, 'birth':birth, 'death':death, 'nationality':nationality}
    
    d = d.append(painter, ignore_index = True)
    print(d)

################################################################################
# This part saves data to csv.
################################################################################
d.to_csv('painters.csv')


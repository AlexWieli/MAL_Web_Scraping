################################################################################
# Scraping Project - My Anime List | Aleksander Wieliński 420272 & Jakub Gazda 419272
################################################################################

from urllib import request
from urllib.parse import quote
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

# Manual limit - increments of 50 are checked
link_limit = 200

while len(anime_links) < link_limit:
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
# This part scraps anime data
################################################################################
d = pd.DataFrame({'title':[], 'type':[], 'episodes':[], 'status':[], 'aired':[], 'studios':[], 'source':[], 'genres':[], 'theme':[], 'demo':[], 'duration':[], 'rating':[], 'score':[], 'ranked':[], 'popularity':[], 'members':[], 'fav':[]})
    
for link in anime_links:
    url = quote(link, safe=':/')
    html=request.urlopen(url)
    bs1=BS(html.read(), 'html.parser')
    print("link: ", link)
    title = bs1.find('h1', {'class':'title-name h1_bold_none'}).get_text(strip=True)

    type = bs1.find('span', string='Type:').find_next_sibling().get_text(strip=True)
    episodes = bs1.find('span', string='Episodes:').parent.get_text(strip=True).replace('Episodes:', '')
    status = bs1.find('span', string='Status:').parent.get_text(strip=True).replace('Status:', '')
    aired = bs1.find('span', string='Aired:').parent.get_text(strip=True).replace('Aired:', '')
    studios = bs1.find('span', string='Studios:').parent.get_text(strip=True).replace('Studios:', '')
    source = bs1.find('span', string='Source:').parent.get_text(strip=True).replace('Source:', '')
    genres = bs1.find('span', string='Genres:').parent.get_text(strip=True).replace('Genres:', '')
    theme = bs1.find('span', string='Theme:').parent.get_text(strip=True).replace('Theme:', '')
    demo = bs1.find('span', string='Demographic:').parent.get_text(strip=True).replace('Demographic:', '')
    duration = bs1.find('span', string='Duration:').parent.get_text(strip=True).replace('Duration:', '')
    rating = bs1.find('span', string='Rating:').parent.get_text(strip=True).replace('Rating:', '')

    score = bs1.find('span', string='Score:').parent.get_text(strip=True).replace('Score:', '')
    ranked = bs1.find('span', string='Ranked:').parent.get_text(strip=True).replace('Ranked:', '')
    popularity = bs1.find('span', string='Popularity:').parent.get_text(strip=True).replace('Popularity:', '')
    members = bs1.find('span', string='Members:').parent.get_text(strip=True).replace('Members:', '')
    fav = bs1.find('span', string='Favorites:').parent.get_text(strip=True).replace('Favorites:', '')

    #anime = {'title':title, 'type':type, 'episodes':episodes}

    anime = {'title':title, 'type':type, 'episodes':episodes, 'status':status, 'aired':aired, 'studios':studios, 'source':source, 'genres':genres, 'theme':theme, 'demo':demo, 'duration':duration, 'rating':rating, 'score':score, 'ranked':ranked, 'popularity':popularity, 'members':members, 'fav':fav}
    
    d = d.append(anime, ignore_index = True)

print(d)
#d.to_csv('anime.csv')

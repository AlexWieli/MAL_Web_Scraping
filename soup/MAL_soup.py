################################################################################
# Scraping Project - My Anime List | Aleksander Wieliński 420272 & Jakub Gazda 419272
################################################################################

from urllib import request
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
import re
import pandas as pd
import time

################################################################################
# This part prepares links to current top anime
################################################################################

Start = time.time()

base_url = 'https://myanimelist.net/'
html = request.urlopen(base_url)
bs = BS(html.read(), 'html.parser')

# Pick Top Anime page

top_url = bs.find('div', {'class': 'footer-ranking'}).div.div.h3.a['href']
html = request.urlopen(top_url)
bs = BS(html.read(), 'html.parser')

# Define links list

anime_links = []

# Scrap links using a certain class in the html code

def scrape_links(url):
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')
    tags = bs.find_all(class_='hoverinfo_trigger fl-l ml12 mr8')
    links = [tag['href'] for tag in tags]
    return links

anime_links.extend(scrape_links(top_url))

# Manual limit - increments of 50 are most easily checked
if True:
    link_limit = 100
else:
    link_limit = 200

# Loop finding the next page, iterating to the next page if the button is found and breaking if its not found. Only applies when link limit is higher than current lenght of the link list

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

# Loop designated for extracting appropriate data from each anime page

for link in anime_links:
    url = quote(link, safe=':/')
    html=request.urlopen(url)
    bs1=BS(html.read(), 'html.parser')

    #time.sleep(2) # delay added as a precaution
    
    title = bs1.find('h1', {'class':'title-name h1_bold_none'}).get_text(strip=True)
    try:
        type = bs1.find('span', string='Type:').find_next_sibling().get_text(strip=True)
    except:
        type = ''
    try:
        episodes = bs1.find('span', string='Episodes:').parent.get_text(strip=True).replace('Episodes:', '')
    except AttributeError:
        episodes = ''
    try:
        status = bs1.find('span', string='Status:').parent.get_text(strip=True).replace('Status:', '')
    except AttributeError:
        status = ''
    try:
        aired = bs1.find('span', string='Aired:').parent.get_text(strip=True).replace('Aired:', '')
    except AttributeError:
        aired = ''
    try:
        studios = bs1.find('span', string='Studios:').parent.get_text(strip=True).replace('Studios:', '')
    except AttributeError:
        studios = ''
    try:
        source = bs1.find('span', string='Source:').parent.get_text(strip=True).replace('Source:', '')
    except AttributeError:
        source = ''
    try:
        genres = ', '.join([a.get_text(strip=True) for a in bs1.find('span', string=re.compile(r'Genre(s)?:$')).parent.find_all('a')])
    except AttributeError:
        genres = ''
    try:
        theme = ', '.join([a.get_text(strip=True) for a in bs1.find('span', string=re.compile(r'Theme(s)?:$')).parent.find_all('a')])
    except AttributeError:
        theme = ''
    try:
        demo = ', '.join([a.get_text(strip=True) for a in bs1.find('span', string='Demographic:').parent.find_all('a')])
    except AttributeError:
        demo = ''
    try:
        duration = bs1.find('span', string='Duration:').parent.get_text(strip=True).replace('Duration:', '')
    except AttributeError:
        duration = ''
    try:
        rating = bs1.find('span', string='Rating:').parent.get_text(strip=True).replace('Rating:', '')
    except AttributeError:
        rating = ''
        
    try:
        score = bs1.find('span', string='Score:').find_next_sibling().get_text(strip=True)
    except AttributeError:
        score = ''
    try:
        ranked_text = bs1.find('span', string='Ranked:').parent.get_text(strip=True).replace('Ranked:', '')
        ranked_number = re.search(r'#(\d+)', ranked_text)
        ranked = ranked_number.group(1)
        ranked = ranked[:-2]
    except AttributeError:
        ranked = ''
    try:
        popularity_text =  bs1.find('span', string='Popularity:').parent.get_text(strip=True).replace('Popularity:', '')
        popularity_number = re.search(r'#(\d+)', popularity_text)
        popularity = popularity_number.group(1)
    except AttributeError:
        popularity = ''
    try:
        members = bs1.find('span', string='Members:').parent.get_text(strip=True).replace('Members:', '')
    except AttributeError:
        members = ''
    try:
        fav = bs1.find('span', string='Favorites:').parent.get_text(strip=True).replace('Favorites:', '')
    except AttributeError:
        fav = ''
    anime = {'title':title, 'type':type, 'episodes':episodes, 'status':status, 'aired':aired, 'studios':studios, 'source':source, 'genres':genres, 'theme':theme, 'demo':demo, 'duration':duration, 'rating':rating, 'score':score, 'ranked':ranked, 'popularity':popularity, 'members':members, 'fav':fav}
    d = pd.concat([d, pd.DataFrame(anime, index=[0])], ignore_index=True)

End = time.time()

print(d)

print('Scraper speed: ', round(End - Start, 2)/60, " minutes.")

d.to_csv('anime_BS.csv')

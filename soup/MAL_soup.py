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
url = 'https://myanimelist.net/' 
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

top_url = bs.find('div', {'class':'footer-ranking'}).div.div.h3.a['href']

html = request.urlopen(top_url)
bs = BS(html.read(), 'html.parser')

tags = bs.find_all(class_='hoverinfo_trigger fl-l ml12 mr8')

anime_links = ['https://myanimelist.net' + tag['href'] for tag in tags]

# debugging print statement
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


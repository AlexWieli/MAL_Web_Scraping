################################################################################
# Scraping Project - My Anime List | Aleksander Wieliński 420272 & Jakub Gazda 419272
################################################################################
# This page exctracts links from wikipedia page in a simplistic way:
from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd

################################################################################
# This part prepares preliminary links - links for lists of links :)
################################################################################
url = 'https://myanimelist.net/' 
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

tags = bs.find_all('a', {'title':re.compile('List of painters by name beginning with.*')})

links = ['http://en.wikipedia.org' + tag['href'] for tag in tags]

################################################################################
# This part prepares real painter links
################################################################################
painter_links = []

for link in links:
    print(link)
    html = request.urlopen(link)
    bs = BS(html.read(), 'html.parser')
    
    tags = bs.find_all('ul')[13].find_all('li')

    link_temp_list = []
    for tag in tags:
        try:
            link_temp_list.append('http://en.wikipedia.org' + tag.a['href'])
        except:
            0 

    painter_links.extend(link_temp_list)

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


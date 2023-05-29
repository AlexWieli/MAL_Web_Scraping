import scrapy
import logging

# a class containing the scrapped data
class AnimeItem(scrapy.Item):
    title = scrapy.Field()
    type = scrapy.Field()
    episodes = scrapy.Field()
    status = scrapy.Field()
    aired = scrapy.Field()
    studios = scrapy.Field()
    source = scrapy.Field()
    genres = scrapy.Field()
    theme = scrapy.Field()
    demo = scrapy.Field()
    duration = scrapy.Field()
    rating = scrapy.Field()
    score = scrapy.Field()
    ranked = scrapy.Field()
    popularity = scrapy.Field()
    members = scrapy.Field()
    fav = scrapy.Field()

# main class
class MyAnimeListSpider(scrapy.Spider):
    name = 'scrapy'
    start_urls = ['https://myanimelist.net/']

    # place where we change the limit of the scrapped animes
    if True:
        link_limit=100
    else:
        link_limit=1000

    # a function that access the ranking page from the main page and sent the link to the next funciton
    def parse(self, response):
        top_url = response.xpath('//div[@class="footer-ranking"]//div//div//h3//a/@href').get()
        yield response.follow(top_url, callback=self.parse_page_links)

    # a function that sends the link to another function of every page with next 50 positions (by chaning the url direcly) given our initial link_limit argument
    def parse_page_links(self, response):
        base_url = response.url
        for i in range(int(self.link_limit//50)):
            url = f"{base_url}?limit={i*50}"
            yield response.follow(url, callback=self.parse_anime_links_page)

    # a function scrapping links from every page with 50 positions and then sening every link to the next function
    def parse_anime_links_page(self, response):
        anime_links = response.xpath('//a[@class="hoverinfo_trigger fl-l ml12 mr8"]/@href').getall()
        
        for link in anime_links:
            logging.info(link)
            yield response.follow(link, callback=self.parse_anime)

    # a function where the link to the page with anime's description is scrapped for basic statistics
    def parse_anime(self, response):
        i = AnimeItem()

        i['title'] = response.xpath('//h1[@class="title-name h1_bold_none"]/strong/text()').get().strip()
        i['type'] = response.xpath("//span[text()='Type:']/following-sibling::*/text()").get().strip()
        i['episodes'] = response.xpath("//span[text()='Episodes:']/following-sibling::text()").get().strip()
        i['status'] = response.xpath("//span[text()='Status:']/following-sibling::text()").get().strip()
        i['aired'] = response.xpath("//span[text()='Aired:']/following-sibling::text()").get().strip()
        i['studios'] = response.xpath("//span[text()='Studios:']/following-sibling::*/text()").get().strip()
        i['source'] = response.xpath("//span[text()='Source:']/following-sibling::text()").get().strip()
        i['genres'] = ', '.join(response.css('span:contains("Genre:") ~ a::text, span:contains("Genres:") ~ a::text').getall())
        i['theme'] = ', '.join(response.css('span:contains("Theme:") ~ a::text, span:contains("Themes:") ~a ::text').getall())
        i['demo'] = ', '.join(response.css('span:contains("Demographic:") ~ a::text').getall())
        i['duration'] = response.xpath("//span[text()='Duration:']/following-sibling::text()").get().strip()
        i['rating'] = response.xpath("//span[text()='Rating:']/following-sibling::text()").get().strip()
        i['score'] = response.xpath("//span[text()='Score:']/following-sibling::*/text()").get().strip()
        i['ranked'] = response.xpath("//span[text()='Ranked:']/following-sibling::text()").get().strip().lstrip('#')
        i['popularity'] = response.xpath("//span[text()='Popularity:']/following-sibling::text()").get().strip().lstrip('#')
        i['members'] = response.xpath("//span[text()='Members:']/following-sibling::text()").get().strip()
        i['fav'] = response.xpath("//span[text()='Favorites:']/following-sibling::text()").get().strip()

        # logging.info(i['title'])
        # logging.info(i['type'])
        # logging.info(i['episodes'])
        # logging.info(i['status'])
        # logging.info(i['aired'])
        # logging.info(i['studios'])
        # logging.info(i['source'])
        # logging.info(i['genres'])
        # logging.info(i['theme'])
        # logging.info(i['demo'])
        # logging.info(i['duration'])
        # logging.info(i['rating'])
        # logging.info(i['score'])
        # logging.info(i['ranked'])
        # logging.info(i['popularity'])
        # logging.info(i['members'])
        # logging.info(i['fav'])

        yield i

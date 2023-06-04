# MAL Web Scraping | AW JG project

# 2. Selenium

In order to use Selenium to run the webpage you need a little bit of own setup. First and foremost, do not forget to change directory of your _geckodriver.exe_.(the 15th line of code). Selenium in this use case is quite tricky, because MyAnimeList unfortunately is a rather weak page and is overloaded by frequent accessing very easily. This means that apart from changing the directory you also need to change the delay between each page is acessed. For a demonstration purpose, a small if statement is left at the end of the code, however for bigger samples it is recommended to set a high delay for each page, and maybe as a precaution a second in between each action, to ensure that the website will have enough time in between animes and won't be overloaded.

# 3. SCRAPY
First access the parent folder containig the spider, and to run the program with a command prompt type "scrapy crawl <spider_name> -O <name_of_the_.csv>". After few seconds the file.csv should be created and ready to be used.

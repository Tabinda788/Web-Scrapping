import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import pandas as pd
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

now = datetime.now()
today = now.strftime("%d/%m/%Y")


display = Display(visible=0, size=(800, 600))
display.start()

def fetch_data():
    class Scrapy_Drugs(scrapy.Spider):
        name = 'Scrapy_Drugs'
        allowed_domains = ['www.webmd.com/drugs/2/index']
        custom_settings = {
            'FEED_FORMAT' : 'csv',
            'FEED_URI' : 'Drugs/drugs.csv',
            'CONCURRENT_REQUESTS_PER_DOMAIN' : 1,
            'DOWNLOAD_DELAY' : 2
        }
        headers = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'}

        start_urls = []
        url_string = "https://www.webmd.com/drugs/2/alpha/"
        for i in range(97,123):
            url_string += chr(i)
            # start_urls.append(url_string)
            for j in range(97,123):
                inner_url_string = url_string + "/" + chr(i)+ chr(j)
                start_urls.append(inner_url_string)
                new_url_string = inner_url_string[:-1]
            url_string = url_string[:-1]

        def parse(self, response):
            scraped_drug_names = response.css('div.drugs-search-list-conditions li a::text').getall()
            # alphabet: response.css('li.sub-alpha-square a::text').get()
            scraped_info = {
                # 'alphabet' : alphabet,
                'Drugs' : scraped_drug_names,
                'date' :today
            }
            yield scraped_info


    if __name__=='__main__':
        process = CrawlerProcess()
        process.crawl(Scrapy_Drugs)
        process.start()

try:
    fetch_data()
except Exception as e:
    print(f'error {e} in fetching the data')

display.stop()

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import pandas as pd


def fetch_data():

    class Scrapy_Articles(scrapy.Spider):
        name = 'Scrapy_Articles'
        allowed_domains = ['www.mayoclinic.org']
        custom_settings = {
            'FEED_FORMAT': 'csv',
            'FEED_URI': 'Articles/articles.csv',
            'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
            'DOWNLOAD_DELAY': 2
        }
        start_urls = ["https://www.mayoclinic.org/diseases-conditions"]

        headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                   'Accept-Language': 'en-US, en;q=0.5'}

        def parse(self, response):

            try:
                disease_or_condition = response.xpath(
                    '//*[@id="mayoform"]/div[6]/header/div/h1/a/text()').get()
            except:
                disease_or_condition = ""

            try:
                text_list = response.css('article').xpath(
                    './/text()').extract()
                cleaned_list = []
                for x in text_list:
                    x = x.replace("\n", "")
                    x = x.replace("\r", "")
                    x = x.replace("\t", "")
                    x = x.replace(",", "")
                    cleaned_list.append(x)

                while("" in cleaned_list):
                    cleaned_list.remove("")

                try:
                    overview_index = cleaned_list.index('Overview')
                    overview = []
                    while cleaned_list[overview_index] != 'Symptoms' and 'Causes' and 'Risk factors' and 'Complications' and 'Prevention':
                        overview_index += 1
                        overview.append(cleaned_list[overview_index])

                    overview = overview[:-1]
                    overview_string = ' '.join(map(str, overview))

                except:
                    overview_string = ""

                try:
                    symptoms_index = cleaned_list.index('Symptoms')
                    symptoms = []
                    while cleaned_list[symptoms_index] != 'Causes' and 'Risk factors' and 'Complications' and 'Prevention':
                        symptoms_index += 1
                        symptoms.append(cleaned_list[symptoms_index])

                    symptoms = symptoms[:-1]
                    symptoms_string = ' '.join(map(str, symptoms))

                except:
                    symptoms_string = ""

                try:
                    cause_index = cleaned_list.index('Causes')
                    causes = []
                    while cleaned_list[cause_index] != 'Risk factors' and 'Complications' and 'Prevention':
                        cause_index += 1
                        causes.append(cleaned_list[cause_index])

                    causes = causes[:-1]
                    causes_string = ' '.join(map(str, causes))

                except:
                    causes_string = ""

                try:
                    risk_index = cleaned_list.index('Risk factors')
                    risk = []
                    while cleaned_list[risk_index] != 'Complications' and 'Prevention':
                        risk_index += 1
                        risk.append(cleaned_list[risk_index])

                    risk = risk[:-1]
                    risk_string = ' '.join(map(str, risk))

                except:
                    risk_string = ""

                try:
                    complications_index = cleaned_list.index('Complications')
                    complications = []
                    while cleaned_list[complications_index] != 'Prevention':

                        complications_index += 1
                        complications.append(cleaned_list[complications_index])

                    complications = complications[:-1]
                    complications_string = ' '.join(map(str, complications))

                except:
                    complications_string = ""

                try:
                    prevention_index = cleaned_list.index('Prevention')
                    preventions = []

                    for prevention in cleaned_list[prevention_index:]:
                        preventions.append(prevention)

                    preventions = preventions[1:]
                    preventions_string = ' '.join(map(str, preventions))

                except:
                    preventions_string = ""
            except:
                pass

            try:
                links = response.css('ol.acces-alpha a::attr(href)').getall()
                articles = response.css('div#index li  a::attr(href)').getall()

                for article in articles:

                    if article is not None:
                        yield response.follow(article, callback=self.parse)

            except:
                print("Didn't get disease urls from this condition response")
            scraped_info = {
                'disease/condition': disease_or_condition,
                'source': 'mayoclinic',
                'overview': overview_string,
                'symptoms': symptoms_string,
                'causes': causes_string,
                'risk_factors': risk_string,
                'complications': complications_string,
                'prevention': preventions_string,
                'url': response.url,

            }
            yield scraped_info
            for next_page in links:

                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)

    if __name__ == '__main__':

        process = CrawlerProcess()
        process.crawl(Scrapy_Articles)
        process.start()


def add_serial():
    data = pd.read_csv(
        '/home/tabinda/Desktop/Web-Scrapping/Articles/articles.csv')
    data.to_csv(
        '/home/tabinda/Desktop/Web-Scrapping/Articles/Articles_scrapped.csv', index_label='s.no')


try:
    fetch_data()
    add_serial()
except Exception as e:
    print(f'error {e} in fetching the data')

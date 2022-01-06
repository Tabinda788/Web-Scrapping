from selenium import webdriver
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options



op = Options()
op.binary_location = "/usr/bin/google-chrome"
chrome_path = r'/home/tabinda/Downloads/chromedriver'
driver = webdriver.Chrome(chrome_path, options=op)
driver.execute_script("window.open('');")
driver.maximize_window()

base_url = 'https://www.realtor.com/realestateandhomes-search/New-York_NY'
for i in range(1, 10):
    drug_url = base_url + '/pg-' + str(i)
    driver.switch_to.window(driver.window_handles[1])
    driver.get(drug_url)
    resp = Selector(text = driver.page_source)
    print(drug_url)
    cards = resp.xpath('//*[@id="srp-body"]/section/ul/li').getall()
    for card in range(len(cards)):
        url = driver.current_url
        price = resp.xpath(f'//*[@id="srp-body"]/section/ul/li[{card}]/div/div[2]/div[4]/div[2]/div/div[1]/span/text()').get()
        status = resp.xpath(f'//*[@id="srp-body"]/section/ul/li[{card}]/div/div[2]/div[4]/div[1]/div/span[2]/text()').get()
        bed = resp.xpath(f'//*[@id="srp-body"]/section/ul/li[{card}]/div/div[2]/div[4]/div[2]/div/div[2]/div/ul/li[1]/span[1]/text()').get()
        bath = resp.xpath(f'//*[@id="srp-body"]/section/ul/li[{card}]/div/div[2]/div[4]/div[2]/div/div[2]/div/ul/li[2]/span[1]/text()').get()
        area = resp.xpath(f'//*[@id="srp-body"]/section/ul/li[{card}]/div/div[2]/div[4]/div[2]/div/div[2]/div/ul/li[3]/span[1]/text()').get()
        area_sq_lot = resp.xpath(f'//*[@id="srp-body"]/section/ul/li[{card}]/div/div[2]/div[4]/div[2]/div/div[2]/div/ul/li[4]/span[1]/text').get()
        adress = resp.xpath(f'//*[@id="srp-body"]/section/ul/li[{card}]/div/div[2]/div[4]/div[2]/div/div[3]/text()').get()
        full_adress = resp.xpath(f'//*[@id="srp-body"]/section/ul/li[{card}]/div/div[2]/div[4]/div[2]/div/div[3]/div/text()').get()
        print(price, status,bed,bath,area,area_sq_lot,adress,full_adress,url)
    

driver.close()






































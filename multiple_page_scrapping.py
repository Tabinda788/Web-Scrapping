from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

user = []
commnent = []

#initialize the driver
driver  = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

# open the product page
url='https://www.sephora.com/product/sephora-collection-hydrate-glow-set-P476487?icid2=value%20sets%20:p476487:product'

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
driver.maximize_window()

driver.get(url)


# scrape the data from page
comments = driver.find_elements_by_xpath('//div[@class="css-k7hahd eanm77i0"]')
user_id = driver.find_elements_by_xpath('//strong[@data-at="nickname"]')


print("printing comments",comments)
# append the data to list
user = []
for i in range(len(user_id)):
    user.append(user_id[i].text)
commnent = []
for i in range(len(comments)):
    commnent.append(comments[i].text)  
# print(user_id)

# navigate between pages

# driver.find_element_by_xpath('//*[@id="ratings-reviews-container"]/div[2]/ul/li[3]/button').click()

data = pd.DataFrame(user)  
data['commnents'] = commnent
data.to_csv('Sentiment.csv',index=False)

driver.close()
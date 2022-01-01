from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# holds an instance for Google Chrome
driver  = webdriver.Chrome(ChromeDriverManager().install())
# driver.maximum window opens chrome on full screen.
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
driver.maximize_window()

driver.get('https://www.naukri.com/data-scientist-jobs?k=data%20scientist')


job_title = driver.find_elements_by_xpath('//a[@class="title fw500 ellipsis"]')

title = []
for i in range(len(job_title)):
     title.append(job_title[i].text)

company = driver.find_elements_by_xpath('//a[@class="subTitle ellipsis fleft"]')

company_ = []
for i in range(len(company)):
    company_.append(company[i].text)

data = pd.DataFrame(title)    
data['company'] = company_
data.to_csv('Job List.csv',index=False)
print(data)

driver.close()
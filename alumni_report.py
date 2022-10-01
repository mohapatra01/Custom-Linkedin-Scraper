import csv
import sys
import fileinput
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import parameters
from parsel import Selector

driver = webdriver.Chrome(parameters.driver_loc)
driver.maximize_window()
sleep(0.5)

driver.get('https://www.linkedin.com/')
sleep(2)
driver.find_element_by_xpath('//a[text()="Sign in"]').click()
sleep(2)
username = driver.find_element_by_name('session_key')
username.send_keys(parameters.username)
sleep(0.5)
password = driver.find_element_by_name('session_password')
password.send_keys(parameters.password)
sleep(0.5)
driver.find_element_by_xpath('//button[text()="Sign in"]').click()
sleep(2)

driver.get('https://www.google.com/')
sleep(2)
search_input = driver.find_element_by_name('q')

beg = 'site:linkedin.com/school'
line = input('Enter the Institute Name\n')
r1 = line.rstrip()
beg = beg + ' AND '
beg = beg +  '"{}"'.format(r1)
search_input.send_keys(beg)
sleep(0.5)
search_input.send_keys(Keys.RETURN)
sleep(2)

schools = driver.find_elements_by_xpath('//*[@class="g"]/*/*/*/a[1]')
school = [school.get_attribute('href') for school in schools]
driver.get(school[0])
sleep(2)

url = driver.current_url.split('?')[0] + 'people/'
driver.get(url)
sel = Selector(text=driver.page_source)
sleep(2)

start_year = 2000
end_year = 2021

url1 = url + "?educationEndYear=" + str(end_year) + "&educationStartYear=" + str(start_year)
driver.get(url1)
sleep(2)
sel = Selector(text=driver.page_source)
sleep(1)

for j in range(3):
    sel = Selector(text=driver.page_source)
    sel1 = sel.xpath('.//*[@class = "insight-container"]')
    for cont in sel1:
        title = cont.xpath('.//h4/text()').extract_first().strip()
        if title == "How you are connected":
            continue
        
        writer = csv.writer(open(line+"-"+title+".csv", 'w', encoding='utf-8'))
        writer.writerow([title,"count"])
        var1 = cont.xpath('.//strong/text()').extract()
        var2 = cont.xpath('.//span/text()').extract()
        var2[0] = var2[0].strip()
        
        if var2[0] == 'Add':
            del var2[0]
        
        num = min(len(var1),len(var2))
        
        for i in range(0,num):
            var1[i] = var1[i].strip()
            var2[i] = var2[i].strip()
            if len(var1[i]) == 0:
                var1[i] = "Not Specified"
            if len(var2[i]) == 0:
                var2[i] = "Not Specified"
            writer.writerow([var2[i],var1[i]])
    
    if j < 2:
        driver.find_element_by_xpath(
            '//button[@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"] ').click()

writer.writerow(["","",""])

driver.quit()

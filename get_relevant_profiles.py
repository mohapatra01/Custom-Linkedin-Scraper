import csv
import parameters
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(parameters.driver_loc)
driver.maximize_window()
sleep(0.5)

driver.get('https://www.linkedin.com/')
sleep(5)

driver.find_element_by_xpath('//a[text()="Sign in"]').click()
sleep(5)

username_input = driver.find_element_by_name('session_key')
username_input.send_keys(parameters.username)
sleep(0.5)

password_input = driver.find_element_by_name('session_password')
password_input.send_keys(parameters.password)
sleep(0.5)

# click on the sign in button
driver.find_element_by_xpath('//button[text()="Sign in"]').click()
sleep(5)

search_input = driver.find_element_by_xpath('//input[@class="search-global-typeahead__input always-show-placeholder"]')
search_query = input('Please Enter the Search Query\n')

writer = csv.writer(open(search_query + "-Data" +'.csv', 'w', encoding='utf-8'))
writer.writerow(['Name', 'Job Title', 'Location', 'Schools', 'Linkedin Url'])

search_input.send_keys(search_query)
sleep(1)

search_input.send_keys(Keys.RETURN)
sleep(6)

profile_urls = []
url = driver.current_url
url = url.replace('linkedin.com/search/results/all', 'linkedin.com/search/results/people')
driver.get(url)
sleep(6)

for i in range(4):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(6)
    profiles = driver.find_elements_by_xpath('//li[@class="reusable-search__result-container "]')

    for profile in profiles:

        try:
            profile.find_element_by_xpath('.//button/span[text()="Connect"]').click()
            sleep(0.5)
            try :
                driver.find_element_by_xpath("//div[@role='dialog']//button/span[text()='Send']").click()
                sleep(0.5)
            except:
                print("Could not Send")
        except:
            print("Could not connect")

        try:
            p_url = profile.find_element_by_xpath('.//a').get_attribute('href')
            if not 'linkedin.com/search' in p_url:
                profile_urls.append(p_url)
        except:
            print("Could not get link")

    if i !=3:
        try:
            driver.find_element_by_xpath("//button/span[text()='Next']").click()
            sleep(6)
        except Exception as f:
            print(f)
            sleep(1000)
            break

for url in profile_urls:
    driver.get(url)
    sleep(5)
    sel = Selector(text=driver.page_source)
    try:
        name = sel.xpath('//h1/text()').extract_first().strip()
        
        job_title = sel.xpath('//main//section//div/h1/../following-sibling::div[1]/text()').extract_first()
        if job_title :
            job_title = job_title.strip()

        schools = sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract()

        location = sel.xpath('//*[@class="text-body-small inline t-black--light break-words"]/text()').extract_first()
        if location:
            location = location.strip()

        ln_url = driver.current_url
        writer.writerow([name, job_title, location, schools, ln_url])
        
    except Exception as e:
        print("We probably landed at a non-profile page")
        print(e)

driver.quit()



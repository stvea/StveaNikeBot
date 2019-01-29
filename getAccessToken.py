import time
import re
import json
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

req_url = 'https://store.nike.com/cn/zh_cn/'
launch_url = 'https://www.nike.com/cn/launch/'
order_url = 'https://store.nike.com/cn/zh_cn/orders/'
login_url = 'https://unite.nike.com/login?'

def getToken(username,password):
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    options.add_experimental_option("prefs",prefs)
    #options.add_argument('headless')
    #options.add_argument('window-size=1200x600')
    driver = webdriver.Chrome(options=options)

    driver.get(req_url)
    try:
        WebDriverWait(driver,20,0.5).until(lambda x:x.find_element_by_xpath('//li[@js-hook="exp-join-login"]').is_displayed())
        #print(driver.current_url)
    except TimeoutException:
        print('time out')
    else:
        driver.find_element_by_xpath('//li[@js-hook="exp-join-login"]').click()
        driver.find_element_by_xpath('//div[@class="mobileNumber-div"]/input').send_keys(username)
        driver.find_element_by_xpath('//form[@id="nike-unite-mobileLoginForm"]//div[contains(@class,"password")]/input').send_keys(password)
        driver.find_element_by_xpath('//div[contains(@class,"mobileLoginSubmit")]').click()
        #if driver.find_element_by_xpath('//li[@class="js-listItem"]//a[@js-hook="logout"]'):
        cookies = driver.get_cookies()
        requests_cookies = {cookie['name']:cookie['value'] for cookie in cookies}
        time.sleep(10)
        driver.get("https://unite.nike.com/session.html")
        userInfo = driver.execute_script(
            "return localStorage.getItem('com.nike.commerce.nikedotcom.web.credential');")
        s = json.loads(userInfo)
        #print(s[1])
        print s['access_token']
        #print cookies
        #driver.get(order_url)
        #print(driver.current_url)
        
        #result = requests.get(req_url,cookies=requests_cookies)
        #result = requests.get(req_url)
        #print(result.url)
        #time.sleep(15)
    finally:
        driver.close()
        driver.quit()

getToken('13951807086','Gechao12')

# -*- coding: UTF-8 -*-
import sys
sys.path.append('./Model')
import time
import re
import json
import requests
from MysqlDao import *
from SqliteDao import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

counts = 0
req_url = 'https://store.nike.com/cn/zh_cn/'
launch_url = 'https://www.nike.com/cn/launch/'
order_url = 'https://store.nike.com/cn/zh_cn/orders/'
login_url = 'https://unite.nike.com/login?'

def getTokenEmail(type,username,password,host='0.0.0.0'):
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    options.add_experimental_option("prefs",prefs)
    options.add_argument("--incognito")
    if host != '0.0.0.0':
        options.add_argument("--proxy-server="+host)
        print '[S]use host'
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(req_url)
    try:
        WebDriverWait(driver,20,0.5).until(lambda x:x.find_element_by_xpath('//li[@js-hook="exp-join-login"]').is_displayed())
    except TimeoutException:
        print('time out')
    else:
        driver.find_element_by_xpath('//li[@js-hook="exp-join-login"]').click()
        driver.find_element_by_link_text('使用电子邮件登录。').click()
        driver.find_element_by_name("emailAddress").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        WebDriverWait(driver,20,0.5).until(lambda x:x.find_element_by_css_selector("[value='登录']").is_displayed())
        driver.find_element_by_css_selector("[value='登录']").click()
        WebDriverWait(driver,20,0.5).until(lambda x:x.find_element_by_css_selector("[value='登录']").is_displayed())
        cookies = driver.get_cookies()
        requests_cookies = {cookie['name']:cookie['value'] for cookie in cookies}
        time.sleep(10)
        driver.get("https://unite.nike.com/session.html")
        userInfo = driver.execute_script(
            "return localStorage.getItem('com.nike.commerce.nikedotcom.web.credential');")
        s = json.loads(userInfo)
    finally:
        driver.close()
        driver.quit()
    return s[type]

def getTokenPhone(type,username,password,host='0.0.0.0'):
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    options.add_experimental_option("prefs",prefs)
    options.add_argument("--incognito")
    if host != '0.0.0.0':
        options.add_argument("--proxy-server="+host)
        print '[S]use host'
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(req_url)
    try:
        WebDriverWait(driver,20,0.5).until(lambda x:x.find_element_by_xpath('//li[@js-hook="exp-join-login"]').is_displayed())
    except TimeoutException:
        print('time out')
    else:
        driver.find_element_by_xpath('//li[@js-hook="exp-join-login"]').click()
        driver.find_element_by_xpath('//div[@class="mobileNumber-div"]/input').send_keys(username)
        driver.find_element_by_xpath('//form[@id="nike-unite-mobileLoginForm"]//div[contains(@class,"password")]/input').send_keys(password)
        driver.find_element_by_xpath('//div[contains(@class,"mobileLoginSubmit")]').click()
        cookies = driver.get_cookies()
        requests_cookies = {cookie['name']:cookie['value'] for cookie in cookies}
        time.sleep(10)
        driver.get("https://unite.nike.com/session.html")
        userInfo = driver.execute_script(
            "return localStorage.getItem('com.nike.commerce.nikedotcom.web.credential');")
        s = json.loads(userInfo)
    finally:
        driver.close()
        driver.quit()
    return s[type]

def refreshToken(accountId,username,password,host='0.0.0.0'):
    global counts
    account = SqliteDao()
    try:
        print "username"+username
        token = getTokenEmail('refresh_token',username,password,host)
    except Exception:
        counts -= 1
        account.sqliteUpdate("UPDATE `nikeaccount` SET `time`='failOnce' WHERE id = "+str(accountId))
        print '[StveaSnkrsBOT]>update fail'
        return
    account.sqliteUpdate("UPDATE `nikeaccount` SET `refreshToken`= '"+token+"',`time`='"+ time.asctime( time.localtime(time.time()) )+"' WHERE id = "+str(accountId))
    print "[StveaSnkrsBOT]Update "+username+"-"+password+" token."
    counts -= 1
    return 

def mulRefreshToken(isHost):
    global counts
    print "[StveaSnkrsBOT]>开始获取Refresh Token"
    account = SqliteDao()
    res = account.sqliteFetch("SELECT * FROM nikeaccount where refreshToken is NULL and phone is NULL")
    for re in res:
        refreshToken(re[0],re[1],re[2])
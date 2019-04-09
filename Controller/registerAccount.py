# -*- coding: UTF-8 -*-
import sys
sys.path.append('./Model')
import re
import MySQLdb
import requests
import time
import string
import random
import json
import xlrd
from getProxy import *
from SqliteDao import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

# yimaToken = "011924223657bbc57ab3c37252e8159369dae533b301"
# req_url = 'https://store.nike.com/cn/zh_cn/'
# phone_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token='+yimaToken+'&itemid=723'
# code_url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token='+yimaToken+'&itemid=723&mobile='
# code_url_back = '&release=1'
# proxyAPI = "https://proxy.horocn.com/api/proxies?order_id=YTDE1626729491855347&num=10&format=json&line_separator=win&can_repeat=no&loc_name=%E6%B1%9F%E8%8B%8F%2C%E4%B8%8A%E6%B5%B7"
# ProxyCount = 0
# ProxyList = []
# MaxProxy = 10

def register(host='0.0.0.0'):
	phoneNumber = requests.get(phone_url).content
	phoneNumber = phoneNumber.split('|')[1]
	options = webdriver.ChromeOptions()
	options.add_argument("--incognito")
	# options.add_argument('--headless')
	prefs = {"profile.managed_default_content_settings.images":2}
	options.add_experimental_option("prefs",prefs)
	# host = getProxy()
	if host != '0.0.0.0':
		ar = "--proxy-server=http://"+host
		print ar
		options.add_argument(ar)
		print '[StveaSnkrsBOT]Use host'
	options.add_argument('window-size=1200x600')
	driver = webdriver.Chrome(options=options)
	driver.get(req_url)
	try:
		WebDriverWait(driver,20,0.5).until(lambda x:x.find_element_by_xpath('//li[@js-hook="exp-join-login"]').is_displayed())
	except TimeoutException:
		print('time out')
		driver.quit()
	else:
		driver.find_element_by_xpath('//li[@js-hook="exp-join-login"]').click()
		driver.find_element_by_link_text('立即加入。').click()
		driver.find_element_by_css_selector("[class='phoneNumber']").send_keys(phoneNumber)
		driver.find_element_by_css_selector("[class='sendCodeButton']").click()
		time.sleep(3)
		email = ''.join(random.sample(string.ascii_letters + string.digits, 8))+'98617@163.com'
		lastN = ''.join(random.sample(string.ascii_letters + string.digits, 3))
		firstN = ''.join(random.sample(string.ascii_letters + string.digits, 3))
		verifyCode = ''
		while 1:
			time.sleep(1)
			verify_url = code_url+phoneNumber+code_url_back
			verifyCode = requests.get(verify_url).content
			if verifyCode.find('success') != -1:
				verifyCode = re.findall("\d+",verifyCode)[0]
				print verifyCode
				break
		try:
			driver.find_element_by_xpath('//div[@class="verifyCode"]/input').send_keys(verifyCode)
			driver.find_element_by_css_selector("[value='继续']").click()
			WebDriverWait(driver,20,0.5).until(lambda x:x.find_element_by_css_selector("div.lastName>input").is_displayed())
			driver.find_element_by_css_selector("div.lastName>input").send_keys(lastN)
			driver.find_element_by_css_selector("div.firstName>input").send_keys(firstN)
			driver.find_element_by_css_selector("div.password>input").send_keys("Aa123456")
			driver.find_element_by_css_selector("div.gender>ul>li").click()
			driver.find_element_by_css_selector("[value='注册']").click()
			WebDriverWait(driver,20,0.5).until(lambda x:x.find_element_by_css_selector("div.emailAddressOptional>input").is_displayed())
			driver.find_element_by_css_selector("div.emailAddressOptional>input").send_keys(email)
			driver.find_element_by_css_selector("[value='保存']").click()
			print email+'!'+'Aa123456'+'!'+phoneNumber
		except Exception:
			driver.quit()
			return 
		else:
			driver.quit()
			return
		mysql = MysqlDao()
		mysql.mysqlUpdate("INSERT INTO `nikeaccount`(`email`, `password`, `phone`) VALUES ('"+email+"','"+'Aa123456'+"','"+phoneNumber+"')")


def registerFromTxt():
	f = open("account.txt","r")
	line = f.readline()
	count = 0
	while line:
		line = line.split(':')
		email = line[0]
		pwd = line[1]
		sql = "INSERT INTO `nikeaccount`(`email`, `password`) VALUES ('"+email+"','"+pwd+"')"
		mysql = SqliteDao()
		mysql.sqliteUpdate(sql)
		count+=1
		line = f.readline()
	f.close()
def registerFromExcel():
	f = xlrd.open_workbook('account.xlsx')
	table = f.sheet_by_index(0)
	nrows = table.nrows
	sqlite = SqliteDao()
	print nrows
	for i in range(nrows):
		email = table.cell(i,0).value
		pwd = table.cell(i,1).value
		sql = "INSERT INTO `nikeaccount`(`email`, `password`) VALUES ('"+email+"','"+pwd+"')"
		sqlite.sqliteUpdate(sql)

def registerFromTxtWithRefreshToken(text):
	f = open("/account-token.txt","r")
	line = f.readline()
	count = 0
	while line:
		line = line.split('!')
		email = line[0]
		pwd = line[1]
		phone = line[2]
		token = line[3]
		sql = "INSERT INTO `nikeaccount`(`email`, `password`, `phone`,`refreshToken`) VALUES ('"+email+"','"+pwd+"','"+phone+"','"+token+"')"
		mysql = SqliteDao()
		mysql.sqliteUpdate(sql)
		count+=1
		text.insert(tk.END,"[StveaSnkrsBOT]>Import "+str(count)+"st Account")
		line = f.readline()
	f.close()

registerFromTxt()
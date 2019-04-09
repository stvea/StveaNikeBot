# -*- coding: UTF-8 -*-
import sys
import time
import requests
sys.path.append('./Model')
from SqliteDao import *
def getEntryResults():
	url = "https://unite.nikecloud.com/tokenRefresh?backendEnvironment=identity&locale=zh_CN&mobile=true&native=true&uxId=com.nike.commerce.snkrs.ios&sdkVersion=2.8.4&backendEnvironment=identity&platform=ios&browser=uniteSDK"
	while 1:
		orders = SqliteDao()
		res = orders.sqliteFetch("SELECT * FROM `nikeorder` where results is null ")
			# where results is null")
		for re in res:
			headers = {"authorization": "Bearer " + re[2]}
			try:
				response = requests.get("https://api.nike.com/launch/entries/v2/" + re[1], headers=headers).json()
			except:
				print "ban ip"
			try:
				if response["waitingReason"]=="OUT_OF_STOCK":
					print "NonWinner" 
					orders.sqliteUpdate("UPDATE `nikeorder` SET `results`='fail' WHERE orderid = '"+re[1]+"'")
				print response["waitingReason"]
			except Exception:
				print response
			try:
				result = response["result"]

			except:
				continue
			if result["status"] == "WINNER":
				print "[StveaSnkrsBot]Draw Enrty username:"+re[5]
				orders.sqliteUpdate("UPDATE `nikeorder` SET `results`='success' WHERE orderid = '"+re[1]+"'")
			elif result["status"] == "NON_WINNER":
				print "NonWinner" 
				orders.sqliteUpdate("UPDATE `nikeorder` SET `results`='fail' WHERE orderid = '"+re[1]+"'")
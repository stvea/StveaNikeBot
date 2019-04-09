# -*- coding: UTF-8 -*-
import sys
sys.path.append('./Model')
import re
import json
import time
import requests
import threading
from iobbgen_ios import *
from NikeAccount import *
from NikeItem import *
from SqliteDao import *
from getProxy import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

UserAgent = "SNKRS/3.7.2 (iPhone; iOS 12.0.1; Scale/2.00)"
XAcfSensorData="1,i,nd4i9ZepIUIjJ2pbeFiG9NPzZo3Zd185BKFfum1J92pknIC4QI555jVGq6v7mX+s+gBZ0kXPjxGD7zD1+uXFO3J63csu+ZV3sQ2SxpGahhfvQ3IisCmUo0YGTAOaVGY3wo1EmUJHvzcvhq7rkL0slrit2VBSssvSOt0Voxy/EGo=,VJmkK8Lshbx+XzbC30C971fzAE9OVCUb2WGqmJwBpvQkynA+G5leN28GaYXTs9vRN9442rNU8aeulwbS0EMK+R8nOHmUEZAIbkgyeSS6+59Hb1hrnduY+eBl0zG+IsWDhMQoyqQwxpoIarUq3qGm8Goj+jV97OFtQaGLmxlZLVc=$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$18,8,26"
xNikeCaller = "nike:snkrs:ios:3.7"
proxyAPI = "https://proxy.horocn.com/api/proxies?order_id=YTDE1626729491855347&num=5&format=json&line_separator=win&can_repeat=no&loc_name=%E6%B1%9F%E8%8B%8F"
MaxProxyCounts = 5
ProxyCount = 0
ProxyList = ['0.0.0.0','0.0.0.0','0.0.0.0','0.0.0.0','0.0.0.0']
EntryList = []
counts = 0
DrawAccounts = 0
EntryAccounts = 0

def getPaymentToken(account,item):
    proxies = {'http': account.host, 'https': account.host}
    url = "https://api.nike.com/payment/preview/v2"
    headers = {
        "Accept": "application/json; charset=utf-8",
        "Authorization": "Bearer " + account.access_token,
        "Content-Type": "application/json",
        "x-nike-caller-id": xNikeCaller,
        'x-acf-sensor-data':XAcfSensorData,
        "User-Agent": UserAgent,
        "X-NewRelic-ID": "VQYGVF5SCBADUVBRBgAGVg=="
    }
    data = {"total": item.price, "items": [{"productId": item.productId,
                                            "shippingAddress": account.addressInfo}],
            "checkoutId": account.checkoutId, "currency": "CNY", "paymentInfo": [
            {"id": account.paymentsId, "type": "Alipay",
             "billingInfo": {"name": account.recipientInfo,
                             "contactInfo": account.contactInfo,
                             "address": account.addressInfo}}], "country": "CN"}
    if account.host == '0.0.0.0':
        try:
            response = requests.post(url, headers=headers, json=data).json()
        except Exception:
            print "[StveaSnkrsBOT]Error>noHost>Connect Payment Token Fail!"
            return
    else:
        try:
            response = requests.post(url, headers=headers, json=data, proxies=proxies).json()
        except Exception:
            print "[StveaSnkrsBOT]Error>Host>Connect Payment Token Fail!"
            return
    try:
        # print response
        paymentToken = response["id"]
        # print "[StveaSnkrsBOT]"+account.username+">Payment Token:"+str(paymentToken)
    except Exception:
        print "[StveaSnkrsBOT]Error>Payment Token Fail:"+str(response)
        return
    return paymentToken

def setCheckoutId(account,item):
    proxies = {'http': account.host, 'https': account.host}
    url = "https://api.nike.com/buy/checkout_previews/v2/" + account.checkoutId
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + account.access_token,
        "Content-Type": "application/json",
        "x-nike-caller-id": xNikeCaller,
        'x-acf-sensor-data':XAcfSensorData,
        "User-Agent": UserAgent,
        "X-NewRelic-ID": "VQYGVF5SCBADUVBRBgAGVg=="
    }
    data = {"request": {"email": "119174379@qq.com",
                        "clientInfo": {"deviceId": "", "client": "com.nike.commerce.snkrs.ios"}, "currency": "CNY",
                        "items": [{"recipient": account.recipientInfo,
                                   "shippingAddress": account.addressInfo,
                                   "id": account.shippingId, "quantity": 1,
                                   "skuId": item.skuId,
                                   "shippingMethod": "GROUND_SERVICE",
                                   "contactInfo": account.contactInfo}],
                       "channel": "SNKRS", "locale": "zh_CN", "country": "CN"}}
    if account.host == '0.0.0.0':
        try:
            response = requests.put(url, headers=headers, json=data).json()
        except Exception:
            print "[StveaSnkrsBOT]Error>noHost>Connect Set Chekout ID Fail!"
            return
    else:
        try:
            response = requests.put(url, headers=headers, json=data, proxies=proxies).json()
        except Exception:
            print "[StveaSnkrsBOT]Error>Host>Connect Set Chekout ID Fail!"
            return
    # print "[StveaSnkrsBOT]"+account.username+">Set Chekout Id response:",
    return response

def getPriceChecksum(account):
    proxies = {'http': account.host, 'https': account.host}
    url = "https://api.nike.com/buy/checkout_previews/v2/jobs/"+account.checkoutId
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + account.access_token,
        "Content-Type": "application/json",
        "x-nike-caller-id": xNikeCaller,
        'x-acf-sensor-data':XAcfSensorData,
        "User-Agent": UserAgent,
        "X-NewRelic-ID": "VQYGVF5SCBADUVBRBgAGVg=="
    }
    if account.host == '0.0.0.0':
        try:
            response = requests.get(url, headers=headers).json()
        except requests.exceptions.Timeout:
            print "[StveaSnkrsBOT]Error>noHost>Timeout>Connect Price CheckSum Fail!"
            return
        except Exception as e:
            print "[StveaSnkrsBOT]Error>noHost>Connect Price CheckSum Fail!"+str(e)
            return
    else:
        try:
            response = requests.get(url, headers=headers,proxies=proxies).json()
        except requests.exceptions.Timeout:
            print "[StveaSnkrsBOT]Error>Host>Timeout>Connect Price CheckSum Fail!"
            return
        except Exception:
            print "[StveaSnkrsBOT]Error>Host>Connect Price CheckSum Fail!"
            return
    try:
        priceChecksum = response["response"]["priceChecksum"]
    except Exception:
        print "[StveaSnkrsBOT]Error>Get Price CheckSum Fail!"+str(response)
        return
    # print "[StveaSnkrsBOT]"+account.username+">priceChecksum:succesee!"+priceChecksum
    return priceChecksum

def launchEntrie(account,item):
    global EntryList
    pTOKEN = getPaymentToken(account,item)
    setCheckoutId(account,item)
    PCS = getPriceChecksum(account)
    # time.sleep(10)
    proxies = {'http': account.host, 'https': account.host}
    url = "https://api.nike.com/launch/entries/v2"
    deviceId = generatefingerprint()
    headers = {
        "Authorization": "Bearer " + account.access_token,
        "Content-Type": "application/json",
        'x-acf-sensor-data':XAcfSensorData,
        "x-nike-caller-id": xNikeCaller,
        "User-Agent":UserAgent,
        "X-NewRelic-ID": "VQYGVF5SCBADUVBRBgAGVg=="
    }
    data = {
    "deviceId": deviceId,
    "postpayLink": item.postpayLink,
    "checkoutId": account.checkoutId,
    "currency": "CNY",
    "paymentToken": pTOKEN,
    "shipping": {
        "recipient": account.launchRecipient,
        "method": "GROUND_SERVICE",
        "address": account.launchAddress
    },
    "skuId": item.skuId,
    "channel": "SNKRS",
    "launchId": item.launchId,
    
    "priceChecksum":PCS,
    "locale": "zh_CN"
    }
    if account.host == '0.0.0.0':
        try:
            response = requests.post(url, headers=headers, json=data).json()
        except requests.exceptions.Timeout:
            print "[StveaSnkrsBOT]Error>noHost>Timeout>Connect Entry Fail!"
            return
        except Exception:
            print "[StveaSnkrsBOT]Error>noHost>Connect Entry Fail!"
            return
    else:
        try:
            response = requests.post(url, headers=headers, json=data, proxies=proxies).json()
        except requests.exceptions.Timeout:
            print "[StveaSnkrsBOT]Error>Host>Timeout>Connect Entry Fail!"
            return
        except Exception:
            print "[StveaSnkrsBOT]Error>Host>Connect Entry Fail!"
            return
    # print  response
    # print "[StveaSnkrsBOT]"+account.username+">Entry response:"
    # try:
    #     print  response["code"]
    #     sna = SqliteDao()
    #     sql = "INSERT INTO `nikeorder`( `orderid`, `accessToken`, `time`,`accountName`) VALUES ('"+response['code']+"','"+account.access_token+"','"+time.asctime( time.localtime(time.time()) )+"','"+account.username+"');"
    #     print sql
    #     sna = sna.sqliteUpdate(sql)
    # except Exception:
    #     print "as"
    try:
        na = SqliteDao()
        sql = "INSERT INTO nikeorder( orderid, accessToken, accountName) VALUES ('"+response['id']+"','"+account.access_token+"','"+account.username+"');"
        na.sqliteUpdate(sql)
        print "[StveaSnkrsBOT]"+account.username+">Entry Success!"
    except Exception:
        print "[StveaSnkrsBOT]Error>"+account.username+">Entry Fail!"+str(response)
        na = SqliteDao()
        sql = "INSERT INTO nikeorder(accountName) VALUES ('fail');"
        na.sqliteUpdate(sql)
    return response

def mulLaunchEntry(nikeitem,useHost=False):
    account = SqliteDao()
    res = account.sqliteFetch("select * from nikeaccount where `token` != ''  ORDER BY accessTime DESC")
    print "[StveaSnkrsBOT]System>Start Entry"
    print "[StveaSnkrsBOT]System>This Task have "+str(len(res))+" accouts"
    if useHost:
        host = getProxy()
    else:
        host = '0.0.0.0'
    for re in res:
        nikeaccount = NikeAccount(re[1],re[2],host,re[5])
        t = threading.Thread(target=launchEntrie,args=(nikeaccount,nikeitem))
        t.start()
        time.sleep(1)
# mulRefreshToken()
# mulAccessToken(False)
# refreshToken("eyJhbGciOiJSUzI1NiIsImtpZCI6IjA3ZmQ4ZGJmLTU3NDktNDlkNC05NDNkLTIzNDIwMmNiYjk3MXNpZyJ9.eyJ0cnVzdCI6MTAwLCJpYXQiOjE1NTE0NTA4MjIsImV4cCI6MTU4Mjk4NjgyMiwiaXNzIjoib2F1dGgyaWR0IiwianRpIjoiOTdkZGEwOWYtYjVkYy00ZTdiLWFkMjItNDY5Yzc0MzhiMmMwIiwibGF0IjoxNTUxNDUwODIyLCJhdWQiOiJvYXV0aDJpZHQiLCJjbGkiOiJIbEhhMkNqZTNjdGxhT3FueHZnWlhOYUFzN1Q5bkF1SCIsInN1YiI6IjA0YjJiMTgwLWJhNmItNDVkOS04ZDlkLTc2NDE5NmQ5ZTg1YyIsInNidCI6Im5pa2U6cGx1cyJ9.fmU7yUpjVigDLXUTBhX8Fx7L1_21EBBz33Jkdvf2WUpsO2SnGdk_y3H0Kkh-a1_Z7d98lZvAvwzR1uT02gBwPaEF52sBvMuxLZYuLC_cwgraP5JQv3YDl8ExoZXaLds00OGudmfjszbygMropCkloi3yDFHPv7q5G3MlGe3rcC1F5fukaluc6-UDQZKkWDBkUBtaWbRQCOnk9hxj7-7rHNWCej-8yA6WEcHuqHnSd5gKJA-7Rp-kNGtaF7MmpR7yQkTOA2bLyexf2H53nlkarjWa7uB6Pm0ILHaJAzYfTeU3UBo7fTksfb8OrX7DLEi63E1kcBzb5_qUcA331XaKiA")
# mulUpdateToken()
# a = NikeAccount("eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc2YWI1NThkLWMwZTMtNGVhYi05MTljLTJkYjA3YjFjN2NhMHNpZyJ9.eyJ0cnVzdCI6MTAwLCJpYXQiOjE1NTEyNzg0MzksImV4cCI6MTU1MTI4MjAzOSwiaXNzIjoib2F1dGgyYWNjIiwianRpIjoiOGYyNjk0ODEtNTg3Ni00YzgwLWEyZmQtOTdlNTQxODhmMTczIiwibGF0IjoxNTUxMjc4NDM5LCJhdWQiOiJjb20ubmlrZS5kaWdpdGFsIiwic3ViIjoiY29tLm5pa2UuY29tbWVyY2UubmlrZWRvdGNvbS53ZWIiLCJzYnQiOiJuaWtlOmFwcCIsInNjcCI6WyJuaWtlLmRpZ2l0YWwiXSwicHJuIjoiODRhM2I0OWMtYTMwOS00YzRlLWI0YmMtOGZkMjlhNDc4OTBjIiwicHJ0IjoibmlrZTpwbHVzIn0.CVeeun03EUVJoNN_AQF2BFF9lIciE7wOCmv3l10ttrdCUGA1w31DjBz7X7-5ELqh_j8M96Y43ReOEAPNocHB1UOXtnKLjsMjEBQc2UDDOZl_XFSaihVQQs16CqwOFo5_7k7Vypz0gdh2Oc1xLLqo8_jomQOmeDECh_IOtWwMx9OsRe3al94IQNg4maBWOM1HTLcOw5g7tat7AKU3LNH48vkz-MV_zOLlnSu7YANFIn-fBXcy3Lxc9jHRP-TBNeOtoZdclG0btoNcX1NY4C7r5AQccispO0SQuP8PBCOZMrIi6rZlSNjNND6ghgE3YN4JCBL0aVQ6afuuUruS1FubQw")
# b = NikeItem("https://www.nike.com/cn/launch/t/vaporfly-4-flyknit-gyakusou-team-red-black-sail/",9,1899)
# b = NikeItem("https://www.nike.com/cn/launch/t/air-zoom-pegasus-35-turbo-gyakusou-gold-dart/",9,1399)
# b = NikeItem("https://www.nike.com/cn/launch/t/womens-m2k-tekno-lx-miami-black-teal-tint-bright-citron/",8.5,899)
# mulLaunchEntrie(b)
# getResults()
# buyCheckouts(a,b)
# print getProxy()
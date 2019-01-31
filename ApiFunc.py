# -*- coding: utf-8 -*-
import time
import re
import json
import requests
from NikeAccount import *
from NikeItem import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

UserAgent = "SNKRS/3.7.2 (iPhone; iOS 12.0.1; Scale/2.00)"
XAcfSensorData="1,i,L5PayBhlnEjJmHxog6XronG54XSceWoGAC6d6lkz+0Una0GEoLSkIZA0PkbIFgYC3/Kgg48wvOkHuB9xry0aOTilmkbeVnZaSalEwz4/2qOyfahgQ4748Rg3YTk03Y0HnWqcgwfGLQrz2YItpoVVaOqdl4f7pGHE95ZDptZqI3s=,o56ITqNSJGtRzW6UtyFOkuQnFwZxo2D5fKVxaxrOS718z537RF8L03xTn34uyTtxWob3eFUcA7Or5l61As7z0HfhohwTiO14F04Ny+2Z1jqtKTOFW+6DVgpg1bakyw4+NsgWC9xWmV2D2RTWQnMhT+WNoqI3wLkxa8bQoPFGwFw=$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$16,9,33"
xNikeCaller = "nike:snkrs:ios:3.7"

def getPaymentToken(account,item):
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
    response = requests.post(url, headers=headers, json=data).json()
    paymentToken = response["id"]
    print "[Stvea Snkrs BOT]>Payment Token:"+paymentToken
    return paymentToken

def setCheckoutId(account,item):
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
    response = requests.put(url, headers=headers, json=data).json()
    print "[Stvea Snkrs BOT]>Set Chekout Id response:",
    print response
    return response

def getPriceChecksum(account):
    url = "https://api.nike.com/buy/checkout_previews/v2/jobs/"+account.checkoutId
    headers = {
        "Accept": "application/json",
        "X-NewRelic-ID": "VQYGVF5SCBADUVBRBgAGVg==",
        "x-nike-caller-id": xNikeCaller,
        'x-acf-sensor-data':XAcfSensorData,
        "Authorization": "Bearer " + account.access_token,
        "User-Agent": UserAgent
    }
    response = requests.get(url, headers=headers).json()
    totalPrice = response["response"]["totals"]["total"]
    priceChecksum = response["response"]["priceChecksum"]
    print "[Stvea Snkrs BOT]>priceChecksum:"+priceChecksum
    return priceChecksum


def launchEntrie(account,item):
    pTOKEN = getPaymentToken(account,item)
    setCheckoutId(account,item)
    PCS = getPriceChecksum(account)
    time.sleep(10)
    url = "https://api.nike.com/launch/entries/v2"
    headers = {
        "Authorization": "Bearer " + account.access_token,
        "Content-Type": "application/json",
        'x-acf-sensor-data':XAcfSensorData,
        "x-nike-caller-id": xNikeCaller,
        "User-Agent":UserAgent,
        "X-NewRelic-ID": "VQYGVF5SCBADUVBRBgAGVg=="
    }
    data = {
    "deviceId": "",
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
    response = requests.post(url, headers=headers, json=data).json()
    print "[Stvea Snkrs BOT]>entry response:",
    print response
    return response

a = NikeAccount("eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc2YWI1NThkLWMwZTMtNGVhYi05MTljLTJkYjA3YjFjN2NhMHNpZyJ9.eyJ0cnVzdCI6MTAwLCJpYXQiOjE1NDg4OTU1NjMsImV4cCI6MTU0ODg5OTE2MywiaXNzIjoib2F1dGgyYWNjIiwianRpIjoiYmEzMDkwMjQtOGM3ZS00NDhlLThmODQtM2E2YzE0M2I2N2IyIiwibGF0IjoxNTQ4ODk1NTYzLCJhdWQiOiJjb20ubmlrZS5kaWdpdGFsIiwic3ViIjoiY29tLm5pa2UuY29tbWVyY2UubmlrZWRvdGNvbS53ZWIiLCJzYnQiOiJuaWtlOmFwcCIsInNjcCI6WyJuaWtlLmRpZ2l0YWwiXSwicHJuIjoiMDRiMmIxODAtYmE2Yi00NWQ5LThkOWQtNzY0MTk2ZDllODVjIiwicHJ0IjoibmlrZTpwbHVzIn0.exsGT3IFmM5B3-GetB6XF3LE3uvhWgwotMJcp-Gqj85-fZoc_JzTY4xLYkbQPVAoVEKiN1Xv6XBkXQ0EgRHGYJYH6WgC6Qh_dT-3ykL3rdJM-iQONM959AmPioTeHy98YM28mfphjdvjsy78MeqvkD_0DnPuSpLaTIczdk7t_dm_8U8UwLtN-Zu35kn1-tL54rVsBR2OLSznAJVPJZJ-o0RrT-T2RXEJ8TkEX7fOej8dSK5adks0YXZ8y1drFlJowbmZy40E4mAjryMh5Q91Sldq-_faaCHZOaj54UoqYiPCp7bfKZo8zRl178vN9azTqQRH--66mDQNae0qIbxm1w")
b = NikeItem("https://www.nike.com/cn/launch/t/womens-air-max-97-ultra-metallic-shine-white",9.5,1199)
launchEntrie(a,b)

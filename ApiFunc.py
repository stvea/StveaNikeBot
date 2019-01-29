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

def getPaymentToken(account,item):
        url = "https://api.nike.com/payment/preview/v2"
        headers = {
            "Accept": "application/json; charset=utf-8",
            "Authorization": "Bearer " + account.access_token,
        "Content-Type": "application/json",
        "x-nike-caller-id": "nike:snkrs:ios:3.3",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79",
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
        print paymentToken
        return paymentToken

def setCheckoutId(account,item):
        url = "https://api.nike.com/buy/checkout_previews/v2/" + account.checkoutId
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + account.access_token,
            "Content-Type": "application/json",
            "x-nike-caller-id": "nike:snkrs:ios:3.7",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79",
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
        print response
        return response

def getPriceChecksum(account):
    url = "https://api.nike.com/buy/checkout_previews/v2/jobs/"+account.checkoutId
    headers = {
        "Accept": "application/json",
        "X-NewRelic-ID": "VQYGVF5SCBADUVBRBgAGVg==",
        "x-nike-caller-id": "nike:snkrs:ios:3.7",
        "Authorization": "Bearer " + account.access_token,
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79"
    }
    response = requests.get(url, headers=headers).json()
    totalPrice = response["response"]["totals"]["total"]
    priceChecksum = response["response"]["priceChecksum"]
    print priceChecksum
    #return totalPrice, priceChecksum


def launchEntrie(account,item):
    setCheckoutId(account,item)
    url = "https://api.nike.com/launch/entries/v2"
    headers = {
        "Authorization": "Bearer " + account.access_token,
        "Content-Type": "application/json",
        "x-nike-caller-id": "nike:snkrs:ios:3.3",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79",
        "X-NewRelic-ID": "VQYGVF5SCBADUVBRBgAGVg=="
    }
    data = {
    "deviceId": "",
    "postpayLink": item.postpayLink,
    "checkoutId": account.checkoutId,
    "currency": "CNY",
    "paymentToken": getPaymentToken(account,item),
    "shipping": {
        "recipient": account.launchRecipient,
        "method": "GROUND_SERVICE",
        "address": account.launchAddress
    },
    "skuId": item.skuId,
    "channel": "SNKRS",
    "launchId": item.launchId,
    "locale": "zh_CN",
    "priceChecksum": getPriceChecksum(account)
    }
    response = requests.post(url, headers=headers, json=data).json()
    print response
    return response

a = NikeAccount("eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc2YWI1NThkLWMwZTMtNGVhYi05MTljLTJkYjA3YjFjN2NhMHNpZyJ9.eyJ0cnVzdCI6MTAwLCJpYXQiOjE1NDg3NzI0MDIsImV4cCI6MTU0ODc3NjAwMiwiaXNzIjoib2F1dGgyYWNjIiwianRpIjoiZmEyMzQ4YjctNzFjYS00OTk0LWIzZmMtMTlkM2E4MGQ4OTJiIiwibGF0IjoxNTQ4NzcyNDAyLCJhdWQiOiJjb20ubmlrZS5kaWdpdGFsIiwic3ViIjoiY29tLm5pa2UuY29tbWVyY2UubmlrZWRvdGNvbS53ZWIiLCJzYnQiOiJuaWtlOmFwcCIsInNjcCI6WyJuaWtlLmRpZ2l0YWwiXSwicHJuIjoiMDRiMmIxODAtYmE2Yi00NWQ5LThkOWQtNzY0MTk2ZDllODVjIiwicHJ0IjoibmlrZTpwbHVzIn0.OI0nOwxRamxQJ2FbAEld6MWarSsAQsaZ7-xJelD0YBXAniJdW06lsqpmCyPxUVg0eguoqZUr6EwkA0v9aCOX0Zm5FMennH5ERyIfBlcbTuoafJTUL_23VeIdrMGGVAUyAm0t5nzFMGh-XU3oL-gB8I07hsyPvG0zQYTQYA2g0YJBTG1XbKNdh1WNctDFlt5MInC9ED39tTzLJ5tnYmo2G2UdBn3b1TZl8y0-Ze7Vjb7s1S0Tc6SE138DZv-FCjWumMXHOOMZw5H2-762E77-du6CsOFxjV5wkTk4XrVI33ICZ1agQUmWNEdBBi6a2Y5ibKvDR_SqNde-lb5yJIDG4w")
b = NikeItem("https://www.nike.com/cn/launch/t/womens-rise-react-flyknit-pink-foam-black-vast-grey",9.5,1399)
launchEntrie(a,b)

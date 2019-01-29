# -*- coding: utf-8 -*-
import time
import re
import json
import requests

class NikeItem:

	def getItemInfo(self,url,shoeSize):
		shoesUrl = url
		response = requests.get(shoesUrl).text
		launchId = re.findall(r"\"launchViewId\":\"(.*?)\"", response, re.S | re.I)[0]
		size = re.findall(r"\"sizes\":(.*?),\"_fetchedAt\"", response, re.S | re.I)[0]
		productId = re.findall(r"product\":{\"productId\":\"(.*?)\"", response, re.S | re.I)[0]
		 #postpayLink = getPostpayLink(productId, shoesLink)
		j_size = json.loads(size)
		return productId,j_size[str(shoeSize)]['skuId'],launchId

	def getPostpayLink(self,productId,shoesLink):
	    url = "https://api.nike.com/merch/products/v2/" + productId
	    response = requests.get(url).json()
	    postpayLink = shoesLink + "?LEStyleColor={styleColor}&LEPaymentType=Alipay".format(
	        styleColor=response["styleColor"])
	    return postpayLink

	def __init__(self,url,size,price):
		NikeItem.url = url
		NikeItem.size = size
		NikeItem.price = price
		NikeItem.productId,NikeItem.skuId,self.launchId = self.getItemInfo(url,size)
		self.postpayLink = self.getPostpayLink(self.productId,self.url)
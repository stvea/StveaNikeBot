import time
import re
import json
import requests
from NikeItem import *

def getPostpayLink(productId, shoesLink):
    url = "https://api.nike.com/merch/products/v2/" + productId
    response = requests.get(url).json()
    postpayLink = shoesLink + "?LEStyleColor={styleColor}&LEPaymentType=Alipay".format(
        styleColor=response["styleColor"])
    print postpayLink
    return postpayLink

b = NikeItem("https://www.nike.com/cn/launch/t/womens-rise-react-flyknit-pink-foam-black-vast-grey",9.5,1399)
getPostpayLink(b.productId,b.url)
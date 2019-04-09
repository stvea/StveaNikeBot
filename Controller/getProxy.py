# _*_ coding:utf-8 _*_

import urllib2
import random,requests,time,re

proxyAPI = "https://proxy.horocn.com/api/proxies?order_id=YTDE1626729491855347&num=5&format=json&line_separator=win&can_repeat=no&loc_name=%E6%B1%9F%E8%8B%8F"
MaxProxyCounts = 5
ProxyCount = 0
ProxyList = ['0.0.0.0','0.0.0.0','0.0.0.0','0.0.0.0','0.0.0.0']
proxyUrl = "http://api3.xiguadaili.com/ip/?tid=558658608095386&num=1&delay=1&filter=on"
wandou = "http://api.wandoudl.com/api/ip?app_key=d0194613527bdce17fa055829abd45fd&pack=0&num=1&xy=1&type=1&lb=\r\n&mr=2&"

def testProxy(host):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    url = 'https://www.nike.com'  
    # proxies是requests中的代理 choice是随机使用一个IP 这里http 和 https最好都写上
    try:
        request = requests.get(url, proxies={'http': host,'https':host}, headers=head,timeout=3) 
    except Exception:
        return False
    return True

def getProxy():
    global ProxyCount
    global ProxyList
    global MaxProxyCounts
    if ProxyCount == 0:
        r = requests.get(proxyAPI).content
        json_str = json.loads(r)
        for h in json_str:
            try:
                host = 'http://'+h['host'] +':'+h['port']
            except Exception:
                continue
            if TestProxy(host):   
                ProxyList[ProxyCount] = host
                ProxyCount += 1
            else:
                continue
        if ProxyCount == 0:
            return getProxy()
    ProxyCount-=1
    return ProxyList[ProxyCount]

def getSingleProxy():
    host = "http://"+requests.get(proxyUrl).content
    if not testProxy(host):
        return getXiguaProxy()
    else:
        return host

def getWandou():
    host = requests.get(wandou).content
    print host
    return host
    if not testProxy(host):
        print "Fail:"+host
        return getWandou()
    else:
        return host
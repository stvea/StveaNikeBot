# -*- coding: UTF-8 -*-
import sys
sys.path.append('./Model')
import ttk
import Tkinter as tk
import requests
import threading
from Tkinter import *
from getProxy import *
from MysqlDao import *
from SqliteDao import *

TimeOut = 5

def accessToken(id,token,isHost):
    url = 'https://api.nike.com/idn/shim/oauth/2.0/token'
    data = {'client_id':'HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH',
    'grant_type':'refresh_token',
    'ux_id':'com.nike.commerce.snkrs.ios',
    'refresh_token':token }
    try:
        if isHost:
            host = getSingleProxy()
            proxies = { "http": host, "https": host } 
            a = requests.post('https://api.nike.com/idn/shim/oauth/2.0/token',json=data,verify=False,proxies=proxies, timeout=TimeOut)
        else:
            a = requests.post('https://api.nike.com/idn/shim/oauth/2.0/token',json=data,verify=False, timeout=TimeOut)
    except Exception:
        print "[StveaSnkrsBOT]"+str(id)+">代理连接失败!"
        return
    try:
        access_token = a.json()['access_token']
    except Exception:
        account = SqliteDao()
        account.sqliteUpdate("UPDATE `nikeaccount` SET `token`= 'fail',`accessTime`='"+ str(time.time())+"' WHERE id = "+str(id))
        print "[StveaSnkrsBOT]"+str(id)+">Update Access Token Fail:"+str(a.json())
        return 
    account = SqliteDao()
    account.sqliteUpdate("UPDATE `nikeaccount` SET `token`= '"+access_token+"',`accessTime`='"+ str(time.time())+"' WHERE id = "+str(id))
    print u"[StveaSnkrsBOT]"+str(id)+">Update Access Token Success!"

def mulAccessToken(isHost):
    account = SqliteDao()
    res = account.sqliteFetch("select * from nikeaccount where `refreshToken` != ''")
    print "[StveaSnkrsBOT]>get "+str(len(res))+" accounts Access Token"
    for re in res:
        accessToken(re[0],re[4],isHost)
    print "[StveaSnkrsBOT]>Finish Getting！"
# -*- coding: utf-8 -*-
import sys
sys.path.append(r'D:\Code\Python\NikeBot V1.1\Model')
import re
import json
import time
import requests
import threading
from iobbgen_ios import *
from NikeAccount import *
from NikeItem import *
from MysqlDao import *

def checkLogin(username,pwd):
	r = requests.post('https://stvea.cn/about.php', data = {'username':username,'pwd':pwd})
	if r.text=='successs':
		return True
	else:
		return False


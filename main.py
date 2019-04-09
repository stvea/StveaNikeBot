# -*- coding: UTF-8 -*-
import sys
sys.path.append('./Controller')
sys.path.append('./Model')
sys.path.append('./View')

from launchEntry import *
from NikeItem import *
from loginUI import *
from getAccessToken import *
from getRefreshToken import *
from registerAccount import *
from getEntryResults import *

global isLogin


def helpInfo():
	print u"--------------------------------"
	print u"         Stvea Nike Bot"
	print u"          Verison 1.2"
	print u"--------------------------------"
	print u"Nike数据库生成于:"
	print u"  "+os.getcwd()
	print u"--------------------------------"
	print u"[0]Exit"
	print u"[1]获得 Access Token"
	print u"[2]获得 Refresh Token by Selenium"
	print u"[3]注册账户 by Selenium"
	print u"[4]导入账户 by Txt"
	print u"[5]开始一次抽签"
	print u"[6]查询抽签结果"
	print u"--------------------------------"

if __name__ == '__main__':
	while 1:
		helpInfo()
		codes = input("[StveaSnkrsBot]User>Choose Code:")
		if codes == 3:
			num = input("[StveaSnkrsBot]User>请选择注册数量:")
			for i in range(num):
				register(getWandou())
		if codes == 1:
			flag = raw_input("[StveaSnkrsBot]User>Use host(y/n):")
			if flag=='y':
				mulAccessToken(True)
			else:
				mulAccessToken(False)
		if codes == 4:
			isHost = raw_input("[StveaSnkrsBot]User>With Token(y/n):")
			if isHost =='y':
				registerFromTxtWithRefreshToken()
			else:
				registerFromTxt()
		if codes == 2:
			isHost = raw_input("[StveaSnkrsBot]User>use host(y/n):")
			if isHost =='y':
				mulRefreshToken(True)
			else:
				mulRefreshToken(False)
		if codes == 6:
			getEntryResults()
		if codes == 5:
			itemUrl = raw_input("[StveaSnkrsBot]User>link:")
			itemSize = input("[StveaSnkrsBot]User>size:")
			itemPrice = input("[StveaSnkrsBot]User>price:")
			isHost = raw_input("[StveaSnkrsBot]User>host(y/n):")
			if isHost =='y':
				isHost = True
			else:
				isHost = False
			item = NikeItem(itemUrl,itemSize,itemPrice)
			mulLaunchEntry(item,isHost)
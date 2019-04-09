# This script is for Iovation iOS SDK version 4.3.0

CURRENCY="CNY"
RESOLUTION="1080X1920"
MODELNO="iPhone7,1"
COUNTRYCODE="cn" #ISO Country Code
MODEL="iPhone"
MEMORY="969"
CPU="arm64v8"  #uname -> machine
LOCALE="zh_CN"
TIMEZONE="Asia/Shanghai"
KERNELVERSION="17.6.0"  #uname -> release
BUNDLENAME="SNKRS"
MOBILENETWORKCODE="15"
PROCESSNAME="SNKRS-inhouse"
VOIPSUPPORTED="1"
FILESYSTEMSIZE="15248"
IOSVERSION="12.0.1"
MOBILECOUNTRYCODE="460" # mobile country code defined in https://www.itu.int/itudoc/itu-t/ob-lists/icc/e212_685.pdf, code 234 is for UK
APPID="com.nike.onenikecommerce"
CURRENTRADIOACCESSTECHNOLOGY="LTE"
CARRIERNAME="China Unicom"


from Crypto.Cipher import AES
import base64,uuid,random,os,datetime
# going to use mac address ranges owned by ASUS and NETGEAR in this script, considering they are International companies manufacturing routers
MACADDRESSRANGES=['00:e0:18', '00:0c:6e', '00:1b:fc', '00:1e:8c', '00:15:f2', '00:23:54', '00:1f:c6', 'f8:32:e4', '38:2c:4a', '60:a4:4c', '70:4d:7b', '88:d7:f6', '00:11:2f', '00:11:d8', '00:17:31', '00:18:f3', '48:5b:39', 'f4:6d:04', '30:85:a9', '1c:b7:2c', '40:16:7e', 'e0:3f:49', '50:46:5d', 'd0:17:c2', '2c:fd:a1', '60:45:cb', '10:7b:44', '04:92:26', '14:da:e9', '00:0e:a6', '00:13:d4', '00:26:18', '00:24:8c', 'bc:ee:7b', '08:60:6e', 'c8:60:00', '38:d5:47', '2c:4d:54', '4c:ed:fb', 'b0:6e:bf', '0c:9d:92', '90:e6:ba', 'bc:ae:c5', '10:bf:48', '14:dd:a9', '08:62:66', 'ac:9e:17', 'f0:79:59', '54:a0:50', '10:c3:7b', '78:24:af', 'd8:50:e6', '74:d0:2b', '9c:5c:8e', '70:8b:cd', '18:31:bf', '2c:56:dc', '00:1a:92', '00:1d:60', '00:22:15', '20:cf:30', 'e0:cb:4e', '1c:87:2c', '30:5a:3a', 'ac:22:0b', '54:04:a6', '34:97:f6', '04:a1:51', 'a4:2b:8c', 'a0:04:60', '9c:3d:cf', '2c:b0:5d', '50:4a:6e', '28:c6:8e', '2c:30:33', '00:14:6c', '00:09:5b', '00:0f:b5', '80:37:73', '40:5d:82', 'c0:ff:d4', '10:da:43', 'b0:39:56', 'c4:3d:c7', 'f8:73:94', '10:0d:7f', '6c:b0:ce', '50:6a:03', 'b0:7f:b9', '08:02:8e', '00:1f:33', 'c0:3f:0e', '00:24:b2', '20:4e:7f', '84:1b:5e', 'a0:21:b7', '00:22:3f', '00:1b:2f', 'e0:91:f5', '74:44:01', 'e0:46:9a', '08:bd:43', 'c4:04:15', '9c:d3:6d', '20:e5:2a', '44:94:fc', '00:8e:f2', 'b0:b9:8a', 'cc:40:d0', '78:d2:94', '3c:37:86', 'e4:f4:c6', '00:1e:2a', '00:18:4d', '00:26:f2', '30:46:9a', '4c:60:de', 'e8:fc:af', '20:0c:c8', 'dc:ef:09', 'a0:63:91', 'a0:40:a0', '8c:3b:ad', '14:59:c0']
def encrypt(x,key,pad=False):
	if pad:
		pad=16-(len(x)%16)
		x=x+chr(pad)*pad
	iv=os.urandom(16)
	y=AES.new(key,AES.MODE_CBC,iv)
	return base64.b64encode(iv+y.encrypt(x))



def generatefingerprint():
	token=encrypt(uuid.uuid4().hex.upper(),'\xd7\xdf\xca2\xd0Vhu\xeb\x06\xa0\xba\n\xa2\x07O\xc1\x8b\xcf\x8f2&t\xc0\x92\xc4\xa5\x0b>\xb4\xe7\xbc')
	data = {
		"CURR": CURRENCY,
		"ICTKN": base64.b64encode('bplist00\xd4\x01\x02\x03\x04\x05\x06\t\nX$versionX$objectsY$archiverT$top\x12\x00\x01\x86\xa0\xa2\x07\x08U$nullO\x10\x14'+os.urandom(20)+'_\x10\x0fNSKeyedArchiver\xd1\x0b\x0cTroot\x80\x01\x08\x11\x1a#-27:@Wilq\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00s'),  # UbiquityIdentityToken(identity token for the icloud account the device is logged into) stored in NSKeyedArchiver format
		"PLUG": str(random.randint(0,1)), # battery state(charging or not)
		"RES": RESOLUTION,
		"MODEL": MODELNO,
		"BATL": "0.{0:02d}".format(random.randint(20,99)), # Battery charge level
		"IDN": os.urandom(16).encode('hex').upper(),  # md5 hash of device name
		"CARCC": COUNTRYCODE,
		"IDM": MODEL,
		"PHYMEM": MEMORY,
		"AID": str(uuid.uuid4()).upper(),  # device IDFA = ASIdentifierManager.sharedManager().advertisingIdentifier.UUIDString
		"BBSC": "iOS",
		"CPU": CPU,
		"SIM": "0",
		"ISBRT": "0.{0:02d}".format(random.randint(30,99)),
		"LANG": LOCALE,
		"TZ": TIMEZONE,
		"KERV": KERNELVERSION,
		"APPV": "19546",
		"LSEN": "1",  # Location service enables
		"APPN": BUNDLENAME,
		"JAIL": "0",
		"CARNC": MOBILENETWORKCODE,    # mobile network code
		"CLIENT_TIME": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z",
		"ICVOIP": VOIPSUPPORTED,
		"EXEN": PROCESSNAME,
		"ASTOKEN": token,
		"KCITOKEN": token,
		"BBRT": str(float(random.randint(10000,100000))/100000),  # time passed since CLIENT_TIME was calculated
		"VID": str(uuid.uuid4()).upper(),   # identifierForVendor
		"IRAD": CURRENTRADIOACCESSTECHNOLOGY,
		"CDTOKEN": token,
		"CARN": CARRIERNAME,
		"IAOR": "portrait",
		"APPID": APPID,
		"DEBUG": "0",
		"UPITOKEN": token,
		"NETS": "{\"pdp_ip4\":{\"mac\":\"00:00:00:00:00:01\"},\"en0\":{\"ips\":[\"fe80::"+"{0:0x}:{1:0x}:{2:0x}:{3:0x}".format(random.randint(0,0xffff),random.randint(0,0xffff),random.randint(0,0xffff),random.randint(0,0xffff))+"\",\"192.168.0."+str(random.randint(1,254))+"\"]},\"utun0\":{\"ips\":[\"fe80::"+"{0:0x}:{1:0x}:{2:0x}:{3:0x}".format(random.randint(0,0xffff),random.randint(0,0xffff),random.randint(0,0xffff),random.randint(0,0xffff))+"\"]},\"pdp_ip2\":{\"mac\":\"00:00:00:00:00:01\"},\"pdp_ip0\":{\"ips\":[\"10."+"{0}.{1}.{2}".format(random.randint(0,0xff),random.randint(0,0xff),random.randint(1,0xfe))+"\"]},\"awdl0\":{\"ips\":[\"fe80::"+"{0:0x}:{1:0x}:{2:0x}:{3:0x}".format(random.randint(0,0xffff),random.randint(0,0xffff),random.randint(0,0xffff),random.randint(0,0xffff))+"\"]},\"pdp_ip1\":{\"mac\":\"00:00:00:00:00:01\"}}",
		"CPUCNT": "2",
		"IDOR": "portrait",
		"KCSTAG": encrypt(uuid.uuid4().hex.upper(),'\xd7\xdf\xca2\xd0Vhu\xeb\x06\xa0\xba\n\xa2\x07O\xc1\x8b\xcf\x8f2&t\xc0\x92\xc4\xa5\x0b>\xb4\xe7\xbc'),
		"UPTIME": "{0}.{1:02d}".format(random.randint(10000,200000),random.randint(1,99)),
		"SSID": os.urandom(16).encode('hex').upper(),  # md5 hash of wifi ssid
		"BSSID": random.choice(MACADDRESSRANGES)+ (":%02x:%02x:%02x" % (random.randint(0,0xff),random.randint(0,0xff),random.randint(0,0xff))),
		"PROX": "1",   # proximity on
		"SDKBN": "1480723456",
		"FSSZ": FILESYSTEMSIZE,      # file system size
		"PRON": PROCESSNAME,
		"OSVER": IOSVERSION,
		"OS": "iOS",
		"SDKVER": "4.3.0",
		"CARMC": MOBILECOUNTRYCODE
	}
	q=["05000033"]
	for p in KEYS:
		q.append("{0:04X}".format(len(p)))
		q.append(p)
		val=data[p]
		q.append("{0:04X}".format(len(val)))
		q.append(val)
	return "0500"+encrypt("".join(q),'\x10\xc5\x14\xfb\xca\xabn=\xcd\x9dF\xb2\x0b\xd4\x03\x05\x88:\xf2J\r\x86#x\x0e\xc4CI\xc6\xa6*p',True)
KEYS=['BBSC', 'BBRT', 'SDKVER', 'SDKBN', 'CLIENT_TIME', 'NETS', 'PROX', 'CDTOKEN', 'IAOR', 'SSID', 'BATL', 'CARNC', 'LSEN', 'KERV', 'CARCC', 'UPTIME', 'AID', 'CPU', 'PHYMEM', 'TZ', 'OS', 'KCSTAG', 'MODEL', 'ICTKN', 'LANG', 'ISBRT', 'APPV', 'FSSZ', 'BSSID', 'APPN', 'APPID', 'KCITOKEN', 'ICVOIP', 'JAIL', 'PRON', 'CURR', 'CARMC', 'CARN', 'EXEN', 'SIM', 'IDOR', 'RES', 'IDM', 'CPUCNT', 'VID', 'UPITOKEN', 'ASTOKEN', 'PLUG', 'IDN', 'DEBUG', 'OSVER']

# print generatefingerprint()
# -*- coding: utf-8 -*-
import uuid
class NikeAccount:
    def __init__(self,username,password,host,access_token):
        self.username = username
        self.password = password
    	self.checkoutId = str(uuid.uuid4())
    	self.paymentsId = str(uuid.uuid4())
    	self.shippingId = str(uuid.uuid4())
        self.host = host
    	self.recipientInfo = {"lastName": 'xx ', "firstName": 'xx '}
    	self.addressInfo = {"state": 'CN-42', "city": 'xx市', "address1": 'xx', "postalCode": "xx","address2": "xx", "county": "xx", "country": "xx"}
        self.access_token = access_token
        self.contactInfo = {"phoneNumber": 'xx', "email": 'xx@qq.com'}
        self.launchRecipient = {"lastName": 'xx', "firstName": 'xx', "email": 'xx@qq.com',"phoneNumber": 'xx'}
        self.launchAddress = {"state": 'CN-42', "city": 'xx市', "address1": 'xx', "county": "xx区", "country": "CN"}
    def setOrderId(id):
    	self.OrderId = id
# -*- coding: utf-8 -*-
import uuid
class NikeAccount:
    def __init__(self,access_token):
    	self.checkoutId = str(uuid.uuid4())
    	self.paymentsId = str(uuid.uuid4())
    	self.shippingId = str(uuid.uuid4())
    	self.recipientInfo = {"lastName": '葛', "firstName": '超'}
    	self.addressInfo = {"state": 'CN-42', "city": '武汉市', "address1": '彭刘杨巷5号', "postalCode": "430060","address2": "123", "county": "武昌区", "country": "CN"}
        self.access_token = access_token
        self.contactInfo = {"phoneNumber": '13951807086', "email": '1191743792@qq.com'}
        self.launchRecipient = {"lastName": '葛', "firstName": '超', "email": '1191743792@qq.com',"phoneNumber": '13951807086'}
        self.launchAddress = {"state": 'CN-42', "city": '武汉市', "address1": '彭刘杨巷5号', "county": "武昌区", "country": "CN"}
    def setEntryId(id):
    	self.setEntryId = id


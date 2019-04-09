# -*- coding: utf-8 -*-


import json
import demjson
res = "{u'skuId':u'2b31bd17-fa20-59e0-a168-ec49e233e15f', u'links': {u'self': {u'ref': u'/launch/entries/v2/2f96e678-3d73-5e31-b9f8-eb1ea43617b0'}}, u'resourceType': u'launchentry', u'estimatedResultAvailability': u'2019-03-05T01:14:09.004Z', u'launchId': u'4564eef2-6dd0-4459-a71c-f0260e7eb07e', u'creationDate': u'2019-03-05T01:14:03.952Z', u'id': u'2f96e678-3d73-5e31-b9f8-eb1ea43617b0', u'postpayLink': u'https://www.nike.com/cn/launch/t/air-max-95-nike-day-black/?LEStyleColor=BQ9131-001&LEPaymentType=Alipay'}"
res = "{'skuId':'2b31bd17-fa20-59e0-a168-ec49e233e15f'}"
res = demjson.decode(res)
print res['skuId']
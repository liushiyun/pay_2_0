# -*- coding: utf-8 -*-

import md5
import sys
from pprint import pprint
import json
import requests
import tornado
from tornado.options import define, options

import unittest

reload(sys)
sys.setdefaultencoding("utf-8")

# class VerifyTradeTest(unittest.TestCase):
#     def setUp(self):
#         self.url = "http://localhost:8888/check"
#         self.payload = {"sign": "",
#                         "mernum": "898110259982676",
#                         "ext1": "",
#                         "ext2": "",
#                         "termid": "68986195",
#                         "reqTime": "20150203143757",
#                         "orderId": 627}

#         self.r   = requests.post(self.url, data=json.dumps(self.payload))
#         self.rdict = json.loads(self.r.text)
#     def tearDown(self):
#         pass

#     def testResponseDes(self):
#         self.assertEqual(self.rdict["responseDes"], u"Pos打款仅在9点到18点开放")

# class VerifyParseRequestTest(unittest.TestCase):
#     def setUp(self):
#         self.url = "http://localhost:8888/check"
#         self.payload = {"sign": "",
#                         "mernum": "898110259982676",
#                         "ext1": "",
#                         "ext2": "",
#                         "termid": "68986195",
#                         "reqTime": "20150203143757",
#                         "orderId": 627}

#         self.r   = requests.post(self.url, data=json.dumps(self.payload)+"你好")
#         self.rdict = json.loads(self.r.text)
#     def tearDown(self):
#         pass

#     def testResponseDes(self):
#         self.assertEqual(self.rdict["responseDes"], u"参数异常不能解析json")

class RequestSuccessTest(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:8888/check"
        self.payload = {"sign": "",
                        "mernum": "898110259982676",
                        "ext1": "",
                        "ext2": "",
                        "termid": "68986195",
                        "reqTime": "20150203143757",
                        "orderId": 627}

        self.r   = requests.post(self.url, data=json.dumps(self.payload))
        self.rdict = json.loads(self.r.text)
    def tearDown(self):
        pass

    def testResponseDes(self):
        self.assertEqual(self.rdict["responseDes"], u"")

        
def main():
    unittest.main()

if __name__ == '__main__':
    main()

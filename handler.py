# -*- coding: utf-8 -*-

import tornado

from aiqier import Executor

class BaseHandler(tornado.web.RequestHandler):
    pass

class TestHandler(BaseHandler):
    '''
    用来测试是可以运行的框架
    '''
    def get(self):
        self.write('HelloWorld!')
        self.finish()

class CheckHandler(BaseHandler):
    def post(self):
        self.set_header("Content-type","application/json")

        executor = Executor(self.request.body)
        ok = executor.execute()
        if ok :
            print u"顺利执行完成"
        else :
            print u"出现错误"
        response = executor.responseJson
        self.write(response)
        self.finish()

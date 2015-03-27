# -*- coding: utf-8 -*-
import sys
import json
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
from   tornado.options import define, options

from handler import TestHandler

from handler import CheckHandler

define("debug", default=True, help="Debug Mode", type=bool)
define('port', default=8888, help='run on the port', type=int)



class Application(tornado.web.Application):
    def __init__(self):
        # 哪里来的访问，来调用这里的url。
        # 这里直接是一个json请求。
        handlers = [
            (r"/", TestHandler),
            (r"/check", CheckHandler),
        ]
        settings = dict(
            app_title=u"tianye",
            xsrf_cookies=False,
            cookie_secret="GDDfdfweilian_tianyue**@&*",
            autoescape=None,
            debug=options.debug,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except Exception, e:
        print(e)

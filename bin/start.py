#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import sys

sys.path.append(sys.path[0].replace("/bin", ""))

from bin.service.Service import *
from bin.service.Html_service import *
from tornado.options import define, options
from bin.init import Init

P = Path.getInstance()
define("port", default=8001, help="run on the given port", type=int)

if __name__ == "__main__":
    Init.Init().init()  # 系统初始化
    tornado.options.parse_command_line()
    print(P.htmlPath)
    app = tornado.web.Application(

        handlers=[(r"/service", Service),
                  (r"/index.html", index),
                  (r"/main.html", main),
                  (r"/interface_statistics.html", interface_statistics),
                  (r"/line_test.html", line_test),
                  (r"/line_data.html", line_data)
                  ],
        template_path=P.htmlPath,
        static_path=P.webPath,
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

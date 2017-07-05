#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import tornado.web
from bin.logic.Service_logic import *
from bin.until import Logger
from bin.until import PR
from bin import until
import json

L = Logger.getInstance()
operator = \
    {
        "logic": Service_logic().logic,
        "xx": Service_logic().xx,
        "line_test": Service_logic().line_test
    }


class Service(tornado.web.RequestHandler):
    def get(self):
        _PR = PR.getInstance()
        try:
            method = self.get_argument('method', '__error__')
            if method == "__error__":
                _PR.setCode(until.Code_METHODERROR)
                _PR.setMsg("method ERROR , not give the method or get the method is __error__")
                return self.write(_PR.getPRBytes())
            data = json.loads(self.get_argument('data', None))
            L.debug("the service request method : " + str(method))
            L.debug("the service request parameter : " + str(data))
            self.write(operator.get(method)(data))
        except Exception as e:
            _PR.setCode(until.Code_EXCEPTION)
            _PR.setMsg("exception ERROR :" + str(e))
            self.write(_PR.getPRBytes())

    def post(self):
        self.get()

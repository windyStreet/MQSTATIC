#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import json
from bin import until


class PR(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.code = until.Code_OK
        self.msg = "ok"
        self.result = None

    @property
    def json(self):
        """JSON format data."""
        json = {
            'code': self.code,
            'msg': self.msg,
            'result': self.result,
        }
        json.update(self.kwargs)
        return json

    def setCode(self, code=1):
        self.code = code
        return self

    def setMsg(self, msg="ok"):
        self.msg = msg
        return self

    def setResult(self, result):
        self.result = result
        return self

    def getCode(self):
        return self.code

    def getMsg(self):
        return self.msg

    def getResult(self):
        return self.result

    def getPRBytes(self):
        return bytes(self.getPRStr(), encoding='utf-8')

    def getPR(self):
        return self

    def getPRStr(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def getInstance():
    return PR()

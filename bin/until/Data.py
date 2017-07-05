#!/usr/bin/env python
# !-*- coding:utf-8 -*-

class Data(object):
    def __init__(self):
        pass


def getD4tArr(len=10, default_value=0):
    arr = []
    for i in range(len):
        arr.append(default_value)
    return arr


def isNone(data):
    try:
        if data is None:
            return True
        elif len(data) == 0:
            return True
    except Exception as e:
        return False

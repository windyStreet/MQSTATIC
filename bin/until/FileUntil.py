#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import codecs
from bin.until import Logger

L = Logger.getInstance()


class FileUntil(object):
    def __init__(self):
        pass

    def createFile(self, path, content):
        try:
            with codecs.open(path, 'w', encoding='utf-8') as tmpFile:
                tmpFile.write(str(content))
        except Exception as e:
            L.error("create %s fail", str(path))
            L.error("errorMsg : %s", e)

    def readFile(self, path):
        data = None
        try:
            with open(path, 'r') as tmpFile:
                data = tmpFile.read()
        except Exception as e:
            L.error("read file [ %s ] not exits", str(path))
            L.error("errMsg: %s", e)
        return data

    def delFile(self, path):
        pass

    def Files(self, path):
        pass


def getInstance():
    return FileUntil()

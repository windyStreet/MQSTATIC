#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import codecs
from bin.until.FormatPrint import FormatPrint
import time
import sys
import os
from bin.until import Path


class FileUntil(object):
    def __init__(self):
        pass

    def createFile(self, path, content):
        try:
            with codecs.open(path, 'w', encoding='utf-8') as tmpFile:
                tmpFile.write(str(content))
        except Exception as e:
            FormatPrint.printFalat('create ' + str(path) + ' fail')
            FormatPrint.printError("errorMsg:" + str(e))

    def readFile(self, path):
        data = None
        try:
            with open(path, 'r') as tmpFile:
                data = tmpFile.read()
        except Exception as e:
            FormatPrint.printError("read [ " + str(path) + " ] not exists")
            FormatPrint.printError("errorMsg:" + str(e))
        return data

    def delFile(self, path):
        pass

    def Files(self, path):
        pass


def getInstance():
    return FileUntil()

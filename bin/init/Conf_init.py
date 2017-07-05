#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import Path
from bin.until import Logger
from bin.until import JsonFileFunc
from bin.logic.func import Conf_func

P = Path.getInstance()
L = Logger.getInstance("init")
J = JsonFileFunc.getInstance()


# 配置文件初始化
class Conf_init(object):
    def start(self):
        L.info("init Conf to memory")
        Conf_func.getInstance().init_conf()
        pass

def getInstance():
    return Conf_init()

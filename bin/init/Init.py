#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin.init import DB_init
from bin.init import MongoDB_log
from bin.init import Conf_init
from bin.until import Logger


L = Logger.getInstance()


class Init(object):
    def __init__(self):
        pass

    def init(self):
        #配置文件初始化
        L.info("conf file init start")
        Conf_init.getInstance().start()
        #数据库数据初始化操作
        L.info("DB init start")
        DB_init.getInstance().start()
        #mongoDB初始化操作
        L.info("receive mongodb log start")
        MongoDB_log.getInstance().start()
        pass

#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.init import MongoDB_log
from bin.logic.func import Conf_func
from bin.logic.func import Statistic_item_func
from bin.logic.func import Statistical_item_func
from bin.until import Logger

L = Logger.getInstance()


class Init(object):
    def init(self):
        # 配置文件初始化
        L.info("conf file init ")

        L.info("conf init into memory , starting...")
        Conf_func.getInstance().init_conf()

        # 初始化数据源
        L.info("start sys , init DB_ds ")
        Conf_func.getInstance().init_DB_ds()

        ####################################################################################

        # 统计信息初始化
        L.info("static data init")

        # 初始化统计项信息
        L.info("init statistical_item , starting...")
        Statistic_item_func.getInstance().init_exist_item()

        # 启动统计计算项任务
        L.info("init compute data task , starting...")
        Statistical_item_func.getInstance().start_compute()
        ####################################################################################

        # 日志接收初始化
        L.info("log receive init")

        L.info("init receive mongodb log , starting...")
        MongoDB_log.getInstance().start()

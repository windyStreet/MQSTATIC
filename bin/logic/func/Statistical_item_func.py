#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import queue
import threading

from bin.until import Mongo
from bin.until import Logger
from bin.logic import BO
from bin import init
from bin.until import Time
from bin.logic.BO import Statistical_item_BO

L = Logger.getInstance()


class Statistical_item_func(object):
    def __init__(self):
        threading.Thread.__init__(self)
        self.step_type_count = 3
        self.queue = queue.Queue(self.step_type_count)
        self.thread_stop = False
    pass

    # 添加统计项内容
    # item{"project_name": "项目名称","statistic_type": "统计类型","statistic_name": "统计名称"}
    def add_statistical_item(self, item):
        statistical_item_instance = Mongo.getInstance(table=BO.BASE_statistical_item)
        statistical_item_collection = statistical_item_instance.getCollection()

        statistical_item_bo = Statistical_item_BO.getInstance()
        statistical_item_bo.set_project_name(item["project_name"])
        statistical_item_bo.set_statistical_type(item["statistic_type"])
        statistical_item_bo.set_statistical_start_time(Time.getNowStr())
        datas = []
        for step in init.CONF_INFO["statical_rule"]["statical_step"]:
            statistical_item_bo.set_statistical_step(step)
            datas.append(statistical_item_bo.json)
        statistical_item_collection.insert_many(datas)

        statistical_item_instance.close()
        L.debug("add statistical item info is %s", datas)

    #启动统计计算项任务
    def start_compute(self):
        t = threading.Thread(target=self.product_consume)
        t.start()
        pass


def getInstance():
    return Statistical_item_func()

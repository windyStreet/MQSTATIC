#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import Logger
from bin.until import Path
from bin.until import JsonFileFunc
from bin.until import Mongo
from bin.init import Statistical_compute_init
from bin.logic.func import Statistic_item_func
from bin.logic.func import Statistical_item_func
import os

L = Logger.getInstance()
J = JsonFileFunc.getInstance()
P = Path.getInstance()
DB_INFO = J.readFile(P.confDirPath + os.sep + "DB.json")


class DB_init(object):
    def __init__(self):
        self.ds_code = None  # 数据源code值（唯一）
        self.project = None  # 项目（唯一）
        pass

    # 初始化Ds 数据库
    def init_DB_ds(self):
        mongo_instance = Mongo.getInstance(table="project_ds", ds='base')
        collection = mongo_instance.getCollection()
        collection.remove({})  # 先删除表中所有数据
        datas = []
        for key in DB_INFO.keys():
            value = DB_INFO[key]['dbname']
            data = {}
            data["ds_code"] = key
            data["project"] = value
            L.info("init DB_ds , insert data: %s : %s", key, value)
            datas.append(data)
        collection.insert_many(datas)
        mongo_instance.close()
        pass

    # 数据库初始化
    def start(self):
        # 初始化数据源
        L.info("start sys , init DB_ds ")
        self.init_DB_ds()

        # 初始化统计项信息
        L.info("start sys , init statistical_item ")
        Statistic_item_func.getInstance().init_exist_item()

        # 启动统计计算项任务
        L.info("start sys , compute all count data ")
        Statistical_item_func.getInstance().start_compute()
        Statistical_compute_init.getInstance().start_init()


def getInstance():
    return DB_init()

# if __name__ == "__main__":
#     DB_init().statistical_item_init()

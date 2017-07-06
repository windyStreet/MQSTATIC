#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import Logger
from bin.until import Mongo
from bin.logic.BO import Statistic_item_BO
from bin.logic import BO
from bin.logic.func import Statistical_item_func

from bin import init

L = Logger.getInstance()


class Statistic_item_func(object):
    def __init__(self):
        pass

    # 初始化已经存在的统计项
    def init_exist_item(self):
        L.info("init exist item data ")
        base_mongo_instance = Mongo.getInstance(table=BO.BASE_statistic_item)
        base_collection = base_mongo_instance.getCollection()
        datas = base_collection.find()
        base_mongo_instance.close()
        for data in datas:
            da = {}
            # '''
            # "project_name":"项目名称",
            # "statistic_type":"统计类型",
            # "statistic_name":"统计名称"
            # '''
            da["project_name"] = data["project_name"]
            da["statistic_type"] = data["statistic_type"]
            da["statistic_name"] = data["statistic_name"]
            init.EXIST_ITEM_DATAS.append(da)
        L.info("init exist item ,init data is : %s", init.EXIST_ITEM_DATAS)
        pass

    # 添加统计项
    # item:{"project_name":"项目名称","statistic_type":"统计类型","statistic_name":"统计名称"}
    def add_item(self, item):
        # 新增一个统计项
        if item is None:
            L.info("add item function , item is empty")
        else:
            # 加入数据库
            base_mongo_instance = Mongo.getInstance(table=BO.BASE_statistic_item)
            base_collection = base_mongo_instance.getCollection()
            bo = Statistic_item_BO.getInstance()
            bo.set_project_name(item["project_name"])
            bo.set_statistic_type(item["statistic_type"])
            bo.set_statistic_name(item["statistic_name"])
            base_collection.insert(bo.json)
            # 加入内存变量中
            init.EXIST_ITEM_DATAS.append(item)
            # 加入统计项中
            Statistical_item_func.getInstance().add_statistical_item(item)

    # 删除一个统计项 [此方法置后处理]
    def del_item(self,item):
        pass

    # 整理统计项 [此方法置后处理]
    # 如果存在重复的统计项，进行去重处理，并对结果数据进行清洗
    def arrangement_item(self):
        pass

    # 统计项是否存在
    def is_exist_item(self, item):
        if item is None:
            L.info("is exist item function , give the item is empty")
            return True
        else:
            # item 处于排除统计项
            if item in init.CONF_INFO["statical_rule"]["except"]:
                return True
            # item 不在统计类型内
            if init.CONF_INFO["statical_rule"]['statical_type'] == "all" or item["statistic_type"] in init.CONF_INFO["statical_rule"]['statical_type']:
                return item in init.EXIST_ITEM_DATAS
            return True

def getInstance():
    return Statistic_item_func()

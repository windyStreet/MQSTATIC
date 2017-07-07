#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import os
from bin import init
from bin.until import Logger
from bin.until import JsonFileFunc
from bin.until import Path
from bin.until import Mongo

P = Path.getInstance()
L = Logger.getInstance()
J = JsonFileFunc.getInstance()


class Conf_func(object):
    # 初始化Ds 数据库
    def init_DB_ds(self):
        mongo_instance = Mongo.getInstance(table="project_ds", ds='base')
        collection = mongo_instance.getCollection()
        collection.remove({})  # 先删除表中所有数据
        datas = []
        for key in init.CONF_INFO["DB"].keys():
            value = init.CONF_INFO["DB"][key]['dbname']
            data = {}
            data["db_name"] = value
            data["ds_code"] = key
            data["project"] = key
            L.info("init DB_ds , db_name is %s , ds_code is %s , project is %s ", value, key, key)
            datas.append(data)
        collection.insert_many(datas)
        mongo_instance.close()
        pass

    # 初始化配置文件
    def init_conf(self):
        conf_path = P.confDirPath
        conf_json = {}
        for file_name in os.listdir(conf_path):
            if file_name == "conf.json":
                continue
            if file_name.endswith(".json"):
                conf_key = file_name.split(".")[0]
                conf_json[conf_key] = J.readFile(conf_path + os.sep + file_name)
        init.CONF_INFO = conf_json
        L.debug("init conf_json info is : %s", conf_json)
        J.createFile(conf_path + os.sep + "conf.json", conf_json)

    # 更新配置文件
    def update_conf(self, conf_file_path, data):
        if data is None:
            L.warning("update conf file , the data is empty ")
        if conf_file_path is None:
            L.error("update conf file , the update file Path not be given ")
            L.critical("update conf file , the update file Path not be given ")
        else:
            # 重写文件
            J.createFile(filePath=conf_file_path, data=data)
            # 更新完配置，重新加载配置文件对象
            self.init_conf()
        pass

    # 是否存在该项目 是否存在该数据库
    def is_exist_project(self, project_name):
        if project_name in init.CONF_INFO["DB"].keys():
            return True
        else:
            return False

    # 添加项目 添加数据库
    def add_project(self, project_name):
        conf_path = P.confDirPath + os.sep + "DB.json"
        data = J.readFile(conf_path)
        base_conf_json = data["base"]
        project_db_con_json = base_conf_json.copy()
        project_db_con_json["dbname"] = "OAMP_" + str(project_name)
        data[project_name] = project_db_con_json
        self.update_conf(conf_file_path=conf_path, data=data)
        self.init_DB_ds()
        pass

    # 获取数据源
    def get_datasource(self, project_name):
        if project_name is None:
            return "base"
        return project_name


def getInstance():
    return Conf_func()


if __name__ == "__main__":
    Conf_func().init_conf()
    print(init.CONF_INFO)

#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import os
from bin import init
from bin.until import Logger
from bin.until import JsonFileFunc
from bin.until import Path

P = Path.getInstance()
L = Logger.getInstance()
J = JsonFileFunc.getInstance()


class Conf_func(object):
    # 初始化配置文件
    def init_conf(self):
        conf_path = P.confDirPath
        conf_json = {}
        for file_name in os.listdir(conf_path):
            if file_name == "conf.json":
                continue
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
            #重写文件
            J.createFile(filePath=conf_file_path, data=data)
            # 更新完配置，重新加载配置文件对象
            self.init_conf()
        pass

def getInstance():
    return Conf_func()


if __name__ == "__main__":
    Conf_func().init_conf()
    print(init.CONF_INFO)

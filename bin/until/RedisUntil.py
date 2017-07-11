#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import json
import redis
from bin import init
from bin.until import Logger
import sys
L = Logger.getInstance()


class RedisUntil(object):
    def __init__(self, db=None):
        # 初始化redis
        redis_conf_object = init.CONF_INFO.get("redisConf")
        if redis_conf_object is 0:
            L.error("init redis , not redisConf info'")
            sys.exc_info(1)
        self.password = redis_conf_object["password"]
        # self.socket_timeout = redisConfObject['socket_timeout']
        self.port = redis_conf_object['port']
        self.host = redis_conf_object['host']
        if db is not None:
            self.db = db
        else:
            self.db = 0
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password)
        pass

    def getRedisInstance(self):
        return redis.Redis(connection_pool=self.pool)


def getInstance(db=None):
    return RedisUntil(db).getRedisInstance()

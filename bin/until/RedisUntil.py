#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import json
import redis
from bin.until import JsonFileFunc
from bin.until import Path


class RedisUntil(object):
    def __init__(self, db=None):
        # 初始化redis
        path = Path.getInstance().confDirPath + "redisConf.json"
        redisConfObject = JsonFileFunc.getInstance().readFile(path)
        self.password = redisConfObject["password"]
        # self.socket_timeout = redisConfObject['socket_timeout']
        self.port = redisConfObject['port']
        self.host = redisConfObject['host']
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

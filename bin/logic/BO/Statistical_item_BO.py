#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import datetime
from bin.until import DBCODE

'''
statistical_item={
          "_id":"主键",
          "project_name":"项目名称",
          "createtime":"数据创建时间",
          "updatetime":"数据更新时间",
          "statistical_type":"统计类型",
          "statistical_lastTime":"最后一次统计时间"，
          "statistical_startTime":"起始统计时间",
          "statistical_step":"统计频率",
          "statistical_name“:"统计名称"
      }
'''


class Statistical_item_BO(object):
    def __init__(self):
        self._id = None
        self.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.update_time = None
        self.project_name = None
        self.statistical_type = None
        self.statistical_start_time = None
        self.statistical_step = None
        self.statistical_name = None

    @property
    def json(self):
        """JSON format data."""
        json = {}
        if self._id is not None:
            json['_id'] = self._id
        if self.create_time is not None:
            json['create_time'] = self.create_time
        if self.update_time is not None:
            json['update_time'] = self.update_time
        if self.project_name is not None:
            json['project_name'] = self.project_name
        if self.statistical_type is not None:
            json['statistical_type'] = self.statistical_type
        if self.statistical_start_time is not None:
            json['statistical_start_time'] = self.statistical_start_time
        if self.statistical_step is not None:
            json['statistical_step'] = self.statistical_step
        if self.statistical_name is not None:
            json['statistical_name'] = self.statistical_name
        return json

    @property
    def update_json(self):
        """JSON format data."""
        update_json = {DBCODE.RELATION_UPDATE: self.json}
        return update_json

    def set_id(self, _id):
        self._id = _id
        return self

    def get_id(self):
        return self._id

    def set_create_time(self, create_time=None):
        if create_time is not None:
            self.create_time = create_time
        else:
            self.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        return self

    def get_create_time(self):
        return self.create_time

    def set_update_time(self, update_time=None):
        if update_time is not None:
            self.update_time = update_time
        else:
            self.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        return self

    def get_update_time(self):
        return self.update_time

    def set_statistical_name(self, statistical_name):
        self.statistical_name = statistical_name
        return self

    def get_statistical_name(self):
        return self.statistical_name

    def set_statistical_step(self, statistical_step):
        self.statistical_step = statistical_step
        return self

    def get_statistical_step(self):
        return self.statistical_step

    def get_statistical_start_time(self):
        return self.statistical_startTime

    def set_statistical_start_time(self, statistical_start_time):
        self.statistical_start_time = statistical_start_time
        return self

    def get_statistical_type(self):
        return self.statistical_type

    def set_statistical_type(self, statistical_type):
        self.statistical_type = statistical_type
        return self

    def get_project_name(self):
        return self.project_name

    def set_project_name(self, project_name):
        self.project_name = project_name
        return self


def getInstance():
    return Statistical_item_BO()

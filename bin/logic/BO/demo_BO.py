#!/usr/bin/env python
# !-*- coding:utf-8 -*-


import datetime
from bin.until import DBCODE

'''
statistic_item={
          "_id":"主键",
          "createtime":"数据创建时间",
          "updatetime":"数据更新时间",
          "project_name":"项目名称",
          "statistic_type":"统计类型",
          "statistic_name":"统计名称"
      }
'''


class Statistic_item_BO(object):
    def __init__(self):
        self._id = None
        self.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.update_time = None
        self.project_name = None
        self.statistic_type = None
        self.statistic_name = None

    pass

    @property
    def json(self):
        """JSON format data."""
        json = {}
        if self._id is not None:
            json['_id'] = self._id
        if self.update_time is not None:
            json['update_time'] = self.update_time
        if self.project_name is not None:
            json['project_name'] = self.project_name
        if self.statistic_type is not None:
            json['statistic_type'] = self.statistic_type
        if self.statistic_name is not None:
            json['statistic_name'] = self.statistic_name
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

    def set_update_time(self, update_time=None):
        if update_time is None:
            self.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            self.update_time = update_time
        return self

    def set_project_name(self, project_name):
        self.project_name = project_name
        return self

    def get_project_name(self):
        return self.project_name

    def set_statistic_type(self, statistic_type):
        self.statistic_type = statistic_type
        return self

    def get_statistic_type(self):
        return self.statistic_type

    def set_statistic_name(self, statistic_name):
        self.statistic_name = statistic_name
        return self

    def get_statistic_name(self):
        return self.statistic_name


def getInstance():
    return Statistic_item_BO()

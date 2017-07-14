#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import DBCODE


class Statistic_res_BO(object):
    def __init__(self):
        '''
            "_id":"id"
            "statistical_project":"统计项目"
            "statistical_type":"统计类型"
            "statistical_time":统计时间,
            "statistical_step":"统计步长"，
            "statistical_count":"统计数量"
            "statistical_name":"统计名称"
        '''
        self._id = None
        self.statistical_project = None
        self.statistical_type = None
        self.statistical_time = None
        self.statistical_step = None
        self.statistical_count = 0
        self.statistical_name = None

    @property
    def json(self):
        """JSON format data."""
        json = {}
        if self._id is not None:
            json['_id'] = self._id
        if self.statistical_project is not None:
            json['statistical_project'] = self.statistical_project
        if self.statistical_type is not None:
            json['statistical_type'] = self.statistical_type
        if self.statistical_time is not None:
            json['statistical_time'] = self.statistical_time
        if self.statistical_type is not None:
            json['statistical_type'] = self.statistical_type
        if self.statistical_step is not None:
            json['statistical_step'] = self.statistical_step
        if self.statistical_count is not None:
            json['statistical_count'] = self.statistical_count
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

    def set_statistical_name(self, statistical_name):
        self.statistical_name = statistical_name
        return self

    def get_statistical_name(self):
        return self.statistical_name

    def get_statistical_project(self):
        return self.statistical_project

    def set_statistical_project(self, statistical_project):
        self.statistical_project = statistical_project
        return self

    def get_statistical_type(self):
        return self.statistical_type

    def set_statistical_type(self, statistical_type):
        self.statistical_type = statistical_type

    def get_statistical_time(self):
        return self.statistical_time

    def set_statistical_time(self, statistical_time):
        self.statistical_time = statistical_time
        return self

    def get_statistical_step(self):
        return self.statistical_step

    def set_statistical_step(self, statistical_step):
        self.statistical_step = statistical_step
        return self

    def get_statistical_count(self):
        return self.statistical_count

    def set_statistical_count(self, statistical_count):
        self.statistical_count = statistical_count
        return self


def getInstance():
    return Statistic_res_BO()

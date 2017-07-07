#!/usr/bin/env python
# !-*- coding:utf-8 -*-

class Statistic_res_BO(object):
    def __init__(self):
        '''
            "statistical_project":"统计项目"
            "statistical_type":"统计类型"
            "statistical_time":统计时间,
            "statistical_step":"统计步长"，
            "statistical_count":"统计数量"
            "statistical_name":"统计名称"
        '''
        self.statistical_project = None
        self.statistical_type = None
        self.statistical_time = None
        self.statistical_step = None
        self.statistical_count = 0
        self.statistical_name = None
        pass

    # 均为必须字段
    def json(self):
        json = {
            "statistical_project": self.statistical_project,
            "statistical_type": self.statistical_type,
            "statistical_time": self.statistical_time,
            "statistical_step": self.statistical_step,
            "statistical_count": self.statistical_count,
            "statistical_name": self.statistical_name
        }
        return json

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

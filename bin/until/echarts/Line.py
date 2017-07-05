#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import datetime
from bin.until import Logger
from bin.until import Time
from bin.until import Mongo
from bin.until import DBCODE
from bin.until import Filter
from bin.logic import BO
from bin.until import Data

L = Logger.getInstance()


class Line(object):
    # search_filter_infos = None, _step = 60, _step_count = 7, _title_text = "数据统计", _type = "line"
    def __init__(self, _search_filter_infos, _title_text, _type, _step=60, _step_count=7):
        self._search_filter_infos = _search_filter_infos
        self._step_count = _step_count
        self._step = _step
        self._title_text = _title_text
        self._type = _type
        self.start_time = None
        self.end_time = None

    def getFileter(self):
        pass

    def getLineChartData(self):
        series = []
        _legend_datas = []
        for key in self._search_filter_infos:
            _legend_data = key
            _legend_datas.append(_legend_data)
            _search_filter_info = self._search_filter_infos[key]
            _project = _search_filter_info['project_name']
            self_collection = _search_filter_info['self_collection']
            _filter_infos = _search_filter_info['filter_infos']
            _statistic_type = _search_filter_info['statistic_type']
            _statistic_name = _search_filter_info['statistic_name']

            self.start_time = Time.getStartTime(step=self._step, step_count=self._step_count)  # 获取起始时间
            is_search_db = False
            for _filter_info in _filter_infos:
                key = _filter_info['key']
                relation = _filter_info['relation']
                value = _filter_info['value']
                if key == 'time' and (relation == DBCODE.GT or relation == DBCODE.GTE):
                    self.start_time = value  # 过滤条件中的起始时间
                elif key == 'time' and (relation == DBCODE.LTE or relation == DBCODE.LT):
                    self.end_time = value  # 过滤条件中的终止时间
                else:
                    is_search_db = True

            times = Time.getComputeTimes(start_time=self.start_time, end_time=self.end_time, step=self._step)
            series_data = []  # y轴上的信息
            if is_search_db is True:  # 多条件查询
                _self_filter = Filter.getInstance()
                _self_filter.filter("project", _project, DBCODE.EQ)
                _self_filter.filter("type", _statistic_type, DBCODE.EQ)
                for _filter_info in _filter_infos:
                    if _filter_info['key'] != 'time':
                        _self_filter.filter(_filter_info['key'], _filter_info['value'], _filter_info['relation'])
                for i in range(len(times) - 1):
                    _self_filter.filter("createtime", times[i], DBCODE.GT)
                    _self_filter.filter("createtime", times[i + 1], DBCODE.LTE)
                    _filter = _self_filter.filter_json()
                    count = self_collection.find(_filter).count()
                    series_data.append(count)
            else:
                # 计划分批次查询
                res_collection = Mongo.getInstance(table=BO.BASE_statistic_res).getCollection()
                res_filter = Filter.getInstance()
                res_filter.filter("statistical_time", times[0], DBCODE.GT)
                res_filter.filter("statistical_time", times[-1], DBCODE.LTE)
                res_filter.filter("statistical_step", self._step, DBCODE.EQ)
                res_filter.filter("statistical_type", _statistic_type, DBCODE.EQ)
                res_filter.filter("statistical_project", _project, DBCODE.EQ)
                if Data.isNone(_statistic_name):
                    _statistic_name = None
                res_filter.filter("statistical_name", _statistic_name, DBCODE.EQ)
                print(res_filter.filter_json())
                ress = res_collection.find(res_filter.filter_json()).sort("statistical_time", -1)  # 计算前半部分值
                self._step_count = len(times) - 1
                series_data = Data.getD4tArr(len=self._step_count, default_value=0)  # 坐标轴上的值
                # 先来尝试组合数据，发现数据无法组合完整时，补充数据
                i = 0
                for res in ress:
                    if i == 0 and ress.count() != (len(times) - 1) and res['statistical_time'] != times[-1]:
                        # 重新补录一个值
                        _self_filter = Filter.getInstance()
                        if not Data.isNone(_statistic_name):
                            _self_filter.filter("name", _statistic_name, DBCODE.EQ)
                        _self_filter.filter("project", _project, DBCODE.EQ)
                        _self_filter.filter("type", _statistic_type, DBCODE.EQ)
                        _self_filter.filter("createtime", times[-2], DBCODE.GT)
                        _self_filter.filter("createtime", times[-1], DBCODE.LTE)
                        _filter = _self_filter.filter_json()
                        count = self_collection.find(_filter).count()
                        series_data[i] = count
                        series_data[i + 1] = res['statistical_count']
                        i = i + 2
                    else:
                        series_data[i] = res['statistical_count']
                        i = i + 1
                series_data.reverse()
            xAxis_data = times[1:]  # 横坐标轴信息[] 时间信息 去掉首要点

            serie = {
                "name": _legend_data,
                "type": self._type,
                "showSymbol":False,
                "smooth":True,
                # "stack": '总量',
                "data": series_data.copy()  # 坐标轴上的值
            }
            series.append(serie)

        _result = {
            "title": {
                "text": self._title_text
            },
            "legend": {
                "data": _legend_datas.copy()
            },
            "xAxis": {
                "data": xAxis_data.copy()
            },
            "series": series
        }
        return _result


def getInsatnce(search_filter_infos=None, _title_text="数据统计", _type="line", _step=60, _step_count=7):
    if search_filter_infos is None:
        L.warn("init Line  , not search_filter_infos par")
        return None
    return Line(search_filter_infos, _title_text, _type, _step, _step_count)

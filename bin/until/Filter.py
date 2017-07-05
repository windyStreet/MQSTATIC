#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import DBCODE


class Filter(object):
    def __init__(self):
        self.key = None
        self.value = None
        self.relation = None
        self.filters = []

    @property
    def json(self):
        """JSON format data."""
        json = {
            'key': self.key,
            'value': self.value,
            'relation': self.relation,
        }
        json.update()
        return json

    def filter(self, key=None, value=None, relation=DBCODE.EQ):
        self.key = key
        self.value = value
        self.relation = relation
        self.filters.append(self.json)
        return self

    def filter_datas(self):
        return self.filters

    # 构造生成 mongodb 查询条件json
    def filter_json(self):
        # 下面的示例演示了如何混合使用$or和$in。
        # db.test.find({"$or": [{"name":{"$in":["stephen","stephen1"]}}, {"age":36}]})
        # 下面的示例返回符合条件age >= 18 && age <= 40的文档。
        # db.test.find({"age":{"$gte":18, "$lte":40}})
        filter_json = {}
        for filter_outer in self.filters.copy():
            filter_outer_key = filter_outer['key']
            filter_outer_value = filter_outer['value']
            filter_outer_relation = filter_outer['relation']
            if filter_outer_relation is DBCODE.EQ:  # 等于
                filter_json[filter_outer_key] = filter_outer_value
                continue
            if filter_outer_relation is DBCODE.NE:  # 不等于
                filter_json[filter_outer_key] = {DBCODE.RELATION_NE: filter_outer_value}
                continue
            if filter_outer_relation is DBCODE.LT:  # 小于
                if filter_outer_key in filter_json.keys():
                    filter_json[filter_outer_key].update({DBCODE.RELATION_LT: filter_outer_value})
                else:
                    filter_json[filter_outer_key] = {DBCODE.RELATION_LT: filter_outer_value}
                continue
            if filter_outer_relation is DBCODE.GT:  # 大于
                if filter_outer_key in filter_json.keys():
                    filter_json[filter_outer_key].update({DBCODE.RELATION_GT: filter_outer_value})
                else:
                    filter_json[filter_outer_key] = {DBCODE.RELATION_GT: filter_outer_value}
                continue
            if filter_outer_relation is DBCODE.LTE:  # 小于等于
                if filter_outer_key in filter_json.keys():
                    filter_json[filter_outer_key].update({DBCODE.RELATION_LTE: filter_outer_value})
                else:
                    filter_json[filter_outer_key] = {DBCODE.RELATION_LTE: filter_outer_value}
                continue
            if filter_outer_relation is DBCODE.GTE:  # 大于等于
                if filter_outer_key in filter_json.keys():
                    filter_json[filter_outer_key].update({DBCODE.RELATION_GTE: filter_outer_value})
                else:
                    filter_json[filter_outer_key] = {DBCODE.RELATION_GTE: filter_outer_value}
                continue
            # --和SQL不同的是，MongoDB的in
            # list中的数据可以是不同类型。这种情况可用于不同类型的别名场景。
            # > db.test.find({"name": {"$in": ["stephen", 123]}})
            if filter_outer_relation is DBCODE.IN:  # in 关系
                if filter_outer_key in filter_json.keys():
                    filter_json[filter_outer_key].update({DBCODE.RELATION_IN: filter_outer_value})
                else:
                    filter_json[filter_outer_key] = {DBCODE.RELATION_IN: filter_outer_value}
                continue

            # --$nin等同于SQL中的not in，同时也是$in的取反。如：
            # > db.test.find({"name": {"$nin": ["stephen2", "stephen1"]}})
            if filter_outer_relation is DBCODE.NIN:  # not in 关系
                if filter_outer_key in filter_json.keys():
                    filter_json[filter_outer_key].update({DBCODE.RELATION_NIN: filter_outer_value})
                else:
                    filter_json[filter_outer_key] = {DBCODE.RELATION_NIN: filter_outer_value}
                continue

            # --下面的示例等同于name = "stephen1" or age = 35
            # > db.test.find({"$or": [{"name": "stephen1"}, {"age": 35}]})
            if filter_outer_relation is DBCODE.OR:  # or 关系
                if filter_outer_key in filter_json.keys():
                    filter_json[DBCODE.RELATION_OR].update({filter_outer_key: filter_outer_value})
                else:
                    filter_json[DBCODE.RELATION_OR] = {filter_outer_key: filter_outer_value}
                continue
                pass

            if filter_outer_relation is DBCODE.NOT:  # not 关系
                if filter_outer_key in filter_json.keys():
                    filter_json[DBCODE.RELATION_NOT].update({filter_outer_key: filter_outer_value})
                else:
                    filter_json[DBCODE.RELATION_NOT] = {filter_outer_key: filter_outer_value}
                continue
                pass

            # for filter_inner in self.filters.copy():
            #     filter_inner_key = filter_outer['key']
            #     filter_inner_value = filter_outer['value']
            #     filter_inner_relation = filter_outer['relation']
            #     if filter_outer_key == filter_inner_key:
            #         print(filter_inner_key)
            '''
            重复的查询条件是不需要过滤的
            '''
        return filter_json


def getInstance():
    return Filter()


if __name__ == "__main__":
    _f = Filter()
    _f.filter("createtime", "2017-01-01", DBCODE.GTE)
    _f.filter("createtime", "2017-02-26", DBCODE.LT)
    # print(_f.json)
    _f.filter("project", "abc", DBCODE.EQ)
    _f.filter("type", ['12', '15', '200'], DBCODE.IN)
    # print(_f.json)
    _filter_datas = _f.filter_datas()
    print(_f.filter_json())

#!/usr/bin/env python
# !-*- coding:utf-8 -*-

# statistical 后台计算

import threading
import time

from bin import init
from bin import logic
from bin.init import RabbitMQ_mongo_log
from bin.logic import BO
from bin.logic.BO import Statistic_res_BO
from bin.logic.BO import Statistical_item_BO
from bin.until import DBCODE
from bin.until import Filter
from bin.until import Logger
from bin.until import Mongo
from bin.until import Time

L = Logger.getInstance("times-task.log")
compute_state_info = {}


class Statistical_compute_func(object):
    def compute_data(self, pars, statistical_step):
        # 修改计算状态 防止重复计算
        compute_state_info[statistical_step]["is_able_run"] = False
        for par in pars:
            project_name = par['project_name']
            statistical_type = par['statistical_type']
            statistical_name = par['statistical_name']
            statistical_start_time = par['statistical_start_time']

            times = Time.getComputeTimes(start_time=statistical_start_time, step=statistical_step)

            ds = logic.project_ds_info[project_name]
            table = project_name + "_" + statistical_type
            # 数据源数据，用于统计数据
            statistical_mongo_instance = Mongo.getInstance(table=table, ds=ds)
            statistical_mongo_collection = statistical_mongo_instance.getCollection()
            documents = []
            last_time = None
            for i in range(1, len(times)):
                last_time = times[i]
                _f = Filter.getInstance()
                _f.filter("type", statistical_type, DBCODE.EQ)
                _f.filter("project", project_name, DBCODE.EQ)
                if statistical_name is not None:
                    _f.filter("name", statistical_name, DBCODE.EQ)
                _f.filter("createtime", times[i - 1], DBCODE.GT)
                _f.filter("createtime", times[i], DBCODE.LTE)
                _filter = _f.filter_json()
                count = statistical_mongo_collection.find(_filter).count()
                document_bo = Statistic_res_BO.getInstance()
                document_bo.setStatistical_project(project_name)
                document_bo.setStatistical_time(times[i])
                document_bo.setStatistical_count(count)
                document_bo.setStatistical_step(statistical_step)
                document_bo.setStatistical_type(statistical_type)
                if statistical_name is not None:
                    document_bo.setStatistical_name(statistical_name)
                documents.append(document_bo.json())
                if len(documents) > init.MAX_INSERT_COUNT:
                    res_mongo_instance = Mongo.getInstance(table=BO.BASE_statistic_res)
                    res_collection = res_mongo_instance.getCollection()
                    res_collection.insert_many(documents=documents)  # 将结果插入到结果表中,防止爆了
                    documents = []
                    res_mongo_instance.close()

            if len(documents) > 0:
                res_mongo_instance = Mongo.getInstance(table=BO.BASE_statistic_res)
                res_collection = res_mongo_instance.getCollection()
                res_collection.insert_many(documents=documents)  # 将结果插入到结果表中
                res_mongo_instance.close()
            else:
                L.debug("statistical_deal ,not get the insert data")

            # 去更新statistical_item表
            if last_time is not None:
                _item_bo_1 = Statistical_item_BO.getInstance()
                _item_bo_1.setStatistical_start_time(last_time)

                _item_mongo_instnce = Mongo.getInstance(table=BO.BASE_statistical_item)
                _item_collection = _item_mongo_instnce.getCollection()
                _item_filter = Filter.getInstance().filter("_id", pars["_id"], DBCODE.EQ)
                _item_collection.update_one(_item_filter.filter_json(), _item_bo_1.update_json)
                # 关闭数据库连接
                _item_mongo_instnce.close()
            else:
                L.debug("statistical_deal ,not get last time")
        # 修改计算状态信息
        compute_state_info[statistical_step]["is_able_run"] = True
        compute_state_info[statistical_step]["run_times"] = int(compute_state_info[statistical_step]["run_times"]) + 1

    def init_compute_state_info(self):
        for statical_step in init.CONF_INFO["statical_rule"]["statical_step"]:
            compute_state_info[statical_step] = {}
            compute_state_info[statical_step]["is_able_run"] = True
            compute_state_info[statical_step]["run_times"] = 0
            compute_state_info[statical_step]["last_run_time"] = Time.getNowTimeStamp()
            compute_state_info[statical_step]["threshold"] = statical_step * 60

    # 通过步长进行任务分配
    def start_compute_by_step(self):
        # 消息队列中无数据时，启动该线程，否则等待
        while True:
            try:
                msg_count = RabbitMQ_mongo_log.getInstance().getQueueMsgCount(queue="Mongodb_log")
                if msg_count < init.START_COMPUTE_COUNT:
                    L.info("the  MQ message count is %d , start compute data ", msg_count)
                    break
                L.info("the  MQ message count is %d , waiting ....", msg_count)
            except Exception as e:
                L.warning(e)
            time.sleep(init.INSERT_INETRVAL_TIME)
        # 可以开始启动计算
        while True:
            for statical_step in init.CONF_INFO["statical_rule"]["statical_step"]:
                # 还是单独查询一把吧，要不这个数据就不完整了
                task_mongo_instance = Mongo.getInstance(table=BO.BASE_statistical_item)
                task_collection = task_mongo_instance.getCollection()
                _filter = Filter.getInstance().filter(key="statical_step", value=statical_step, relation=DBCODE.EQ).filter_json()
                statistical_datas = task_collection.find(_filter).sort("statistical_step", 1)
                task_mongo_instance.close()

                # 判断是否需要进行计算
                compute_state_info[statical_step]["interval_time"] = statical_step * 60
                compute_state_info[statical_step]["threshold"] = statical_step * 60 - 5
                now_time_stamp = Time.getNowTimeStamp()
                last_run_time_stamp = compute_state_info[statical_step]["last_run_time"]
                threshold_time_stamp = compute_state_info[statical_step]["threshold"]
                if compute_state_info[statical_step]["is_able_run"] is False or (now_time_stamp - last_run_time_stamp) > threshold_time_stamp:
                    continue
                else:
                    compute_state_info[statical_step]["last_run_time"] = now_time_stamp
                    t = threading.Thread(target=self.compute_data, args=(statistical_datas, statical_step))
                    t.start()
                    # 启动一个线程进行处理,处理完成如何进行休眠或者进行下一次数据处理（其中下一次数据处理的参数会发生变更）
            time.sleep(init.COMPUTE_DATA_INERVAL_TIME)
        pass

    # 计算全部定时任务内容代码开始启动 (启动一个线程来进行处理)
    def start_init(self):
        self.init_compute_state_info()
        t = threading.Thread(target=self.start_compute_by_step)
        t.start()


def getInstance():
    return Statistical_compute_func()

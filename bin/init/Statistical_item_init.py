#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import threading
import queue
import time
from bin.until import Mongo
from bin.logic import BO


class Statistical_item_init(threading.Thread):
    def __init__(self):
        pass
        # threading.Thread.__init__(self)
        # self.queue = queue
        # self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            print("thread%d %s: waiting for tast" % (self.ident, self.name))
            try:
                task = q.get(block=True, timeout=20)  # 接收消息
            except queue.Empty:
                print("Nothing to do!i will go home!")
                self.thread_stop = True
                break
            print("task recv:%s ,task No:%d" % (task[0], task[1]))
            print("i am working")
            time.sleep(3)
            print("work finished!")
            q.task_done()  # 完成一个任务
            res = q.qsize()  # 判断消息队列大小
            if res > 0:
                print("fuck!There are still %d tasks to do" % (res))

    def stop(self):
        self.thread_stop = True

    #启动初始化统计项工作
    def start_init(self):
        #初始化
        pass

def getInstance():
    return Statistical_item_init()


if __name__ == "__main__":
    # q = queue.Queue(3)
    # worker = worker(q)
    # worker.start()
    # q.put(["produce one cup!", 1], block=True, timeout=None)  # 产生任务消息
    # q.put(["produce one desk!", 2], block=True, timeout=None)
    # q.put(["produce one apple!", 3], block=True, timeout=None)
    # q.put(["produce one banana!", 4], block=True, timeout=None)
    # q.put(["produce one bag!", 5], block=True, timeout=None)
    # print("***************leader:wait for finish!")
    # q.join()  # 等待所有任务完成
    # print("***************leader:all task finished!")
    collection = Mongo.getInstance(table=BO.BASE_statistic_res).getCollection()
    # count = collection.find({'statistical_time': {'$gt': '2017-05-16 11:25:00', '$lte': '2017-05-23 10:05:00'}, 'statistical_step': 1, 'statistical_type': 'interface', 'statistical_project': 'YXYBB','statistical_name':None}).count()
    count = collection.find({'statistical_step': 1, 'statistical_project': 'YXYBB', 'statistical_time': {'$lte': '2017-05-23 11:42:00', '$gt': '2017-05-16 13:02:00'}, 'statistical_type': 'interface', 'statistical_name': None}).count()
    print(count)

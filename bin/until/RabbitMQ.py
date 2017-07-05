#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import pika

# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # auth : pangguoping
# import pika
# # ######################### 生产者 #########################
# credentials = pika.PlainCredentials('admin', 'admin')
# #链接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）
# connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.103',5672,'/',credentials))
# #创建频道
# channel = connection.channel()
# # 声明消息队列，消息将在这个队列中进行传递。如果将消息发送到不存在的队列，rabbitmq将会自动清除这些消息。如果队列不存在，则创建
# channel.queue_declare(queue='hello')
# #exchange -- 它使我们能够确切地指定消息应该到哪个队列去。
# #向队列插入数值 routing_key是队列名 body是要插入的内容
#
# channel.basic_publish(exchange='',
#                   routing_key='hello',
#                   body='Hello World!')
# print("开始队列")
# #缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
# connection.close()

from bin.until import JsonFileFunc
from bin.until import Path
import time
import os
from bin.until import Mongo
from bin.until import Logger
from bin.logic import Statistics_BO
import json

L = Logger.getInstance()
P = Path.getInstance()
J = JsonFileFunc.getInstance()

path = P.confDirPath + os.sep + "rabbitMQ.json"
MQ_conf_info = J.readFile(path)


class RabbitMQ(object):
    def __init__(self):
        ip = MQ_conf_info['ip']
        port = None
        user = MQ_conf_info['user']
        password = MQ_conf_info['password']
        credentials = pika.PlainCredentials(user, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port, '/', credentials))
        pass

    def recvMsg(self, queue="Mongodb_log", callback=None):
        if callback is None:
            L.warning("callback method is None")
        channel = self.connection.channel()
        # 声明消息队列，消息将在这个队列中进行传递。如果队列不存在，则创建
        channel.queue_declare(queue=queue, durable=True)

        # 告诉rabbitmq使用callback来接收信息
        channel.basic_consume(callback,
                              queue=queue,
                              no_ack=True)
        # 公平分发，使每个consumer在同一时间最多处理一个message，收到ack前，不会分配新的message
        channel.basic_qos(prefetch_count=10)
        channel.start_consuming()

        # cha = con.channel()
        # # 创建队列anheng
        # result = cha.queue_declare(queue='anheng', durable=True)
        # # 创建名为yanfa,类型为fanout的交换机，其他类型还有direct和topic
        # cha.exchange_declare(durable=False,
        #                      exchange='yanfa',
        #                      type='direct', )
        # # 绑定exchange和queue,result.method.queue获取的是队列名称
        # cha.queue_bind(exchange='yanfa',
        #                queue=result.method.queue,
        #                routing_key='', )
        # # 公平分发，使每个consumer在同一时间最多处理一个message，收到ack前，不会分配新的message
        # cha.basic_qos(prefetch_count=)

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        print(str(body, encoding="utf-8"))
        collection = Mongo.getInstance(table="YXYBB_interface", dbname="YXYBB").collection
        collection.insert(json.loads(str(body, encoding="utf-8")))
        # _data = Statistics_BO.getInstance().setName("YXYBB_interface").setType("interface").setContent(json.loads(str(body, encoding="utf-8"))).json
        # collection.insert(_data)


def getInstance():
    return RabbitMQ()


if __name__ == "__main__":
    RabbitMQ().recvMsg(queue="Mongodb_log", callback=RabbitMQ().callback)

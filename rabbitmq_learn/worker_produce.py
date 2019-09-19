# !/usr/bin/python3
# -*- coding:utf-8 -*-
# @time : 2019.09.06
# @IDE : pycharm
# @auto : jeff_hua
# @github : https://github.com/Jeffer-hua

import time
import pika


def load_channel(queue_name):
    is_connection = True
    while is_connection:
        try:
            user_pwd = pika.PlainCredentials('rabbitmq', 'rabbitmq')
            # 创建连接对象
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=user_pwd,
                                          heartbeat_interval=0))
            # 创建频道对象
            channel = connection.channel()
            # 切换到指定的队列,如果不存在则创建
            channel.queue_declare(queue=queue_name, durable=True)
            is_connection = False
            return channel, connection
        except Exception as e:
            time.sleep(5)
            print(e)


queue_name = 'test'
channel, connection = load_channel(queue_name)

channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body="hello word",
                      # make message persistent
                      properties=pika.BasicProperties(delivery_mode=2))

print("send hello world")
connection.close()

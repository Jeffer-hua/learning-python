# !/usr/bin/python3
# -*- coding:utf-8 -*-
# @time : 2019.09.06
# @IDE : pycharm
# @auto : jeff_hua
# @github : https://github.com/Jeffer-hua

import time
import pika


def load_channel():
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
            channel.exchange_declare(exchange='practice', exchange_type='fanout')
            is_connection = False
            return channel, connection
        except Exception as e:
            time.sleep(5)
            print(e)


channel, connection = load_channel()
channel.basic_publish(
    exchange='practice',
    routing_key='',
    body="hello word"
)

print("send hello world")
connection.close()

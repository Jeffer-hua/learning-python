# !/usr/bin/python3
# -*- coding:utf-8 -*-
# @time : 2019.09.06
# @IDE : pycharm
# @auto : jeff_hua
# @github : https://github.com/Jeffer-hua

import pika
import time


def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("{0}".format(body))


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
            channel.basic_consume(
                queue=queue_name,
                # 回调函数
                consumer_callback=callback,
                no_ack=False
            )

            is_connection = False
            return channel, connection
        except Exception as e:
            time.sleep(5)
            print(e)


queue_name = 'test'
channel, connection = load_channel(queue_name)
channel.start_consuming()

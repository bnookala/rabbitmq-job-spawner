#!/usr/bin/env python

import pika
import sys
import random
import os
import json

credentials = pika.PlainCredentials('user', 'password')
parameters = pika.ConnectionParameters("104.40.75.96", 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue="workqueue",)

iterations = 1

for i in range(iterations):
    message = {
        'input_blob_loc': 'dataporter/in/300MB_1865981128.dat',
        'output_blob_loc': 'dataporter',
        'output_file_name': 'output/300MB_1865981128.out'
    }

    channel.basic_publish(
        exchange='',
        routing_key="workqueue",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )

    print(" [x] Sent message")

channel.close()
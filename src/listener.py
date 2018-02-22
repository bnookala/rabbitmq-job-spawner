# -*- coding: utf-8 -*-

import requests
import time
import os
import json
import pika

import pykube


class Listener(object):

    def __init__(self):
        # Set this environment variable on the cluster to tell PyKube to load
        # secrets from Kubernetes.
        if os.environ.get('KUBERNETES', None):
            self.api = pykube.HTTPClient(
                pykube.KubeConfig.from_service_account()
            )
        else:
            self.api = pykube.HTTPClient(
                pykube.KubeConfig.from_file(os.environ['KUBECONFIG'])
            )

        if not os.environ['RABBIT_PASSWORD']:
            print("RABBIT_PASSWORD not set in environment")
            return

        if not os.environ['RABBIT_URL']:
            print("RABBIT_URL not set in environment")
            return

        if not os.environ['PORT']:
            print("PORT not set in environment")
            return

        if not os.environ['QUEUE']:
            print("QUEUE not set in environment")
            return

        if not os.environ['WORKLOAD']:
            print("WORKLOAD not set in environment")
            return

        credentials = pika.PlainCredentials(
            'user',
            os.environ['RABBIT_PASSWORD']
        )

        parameters = pika.ConnectionParameters(
            os.environ['RABBIT_URL'],
            os.environ['PORT'],
            '/',
            credentials
        )

        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue=os.environ['QUEUE']
        )

    # Spawns a job based on the queue.
    def callback(self, ch, method, properties, body):
        try:
            payload = str(body, 'utf-8')
            message_obj = json.loads(payload)
        except Exception:
            print("Queued object could not be loaded: ")
            print(body)
            return

        # example… workload (fix this later)
        encoding_type = message_obj.get('encoding_type')
        file_name = message_obj.get('file_name')
        file_loc = message_obj.get('file_loc')

        self.create_job_with_message(encoding_type, file_name, file_loc)

        # todo: confirm where we should actually do this.
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def create_job_with_message(self, file_name, file_loc, encoding_type):
        # todo: set the arguments as environment variables on the workload…

        spec_file = os.getcwd() + '/workloads/' + os.environ.get('WORKLOAD')

        with open(spec_file, 'r') as spec:
            lines = spec.read()
            json_spec = json.loads(lines)

        pykube.Job(self.api, json_spec).create()

    def start_consume(self):
        self.channel.basic_consume(
            self.callback,
            queue=os.environ['QUEUE']
        )

        self.channel.start_consuming()
        print(' [*] Waiting for messages. To exit press CTRL+C')

if __name__ == "__main__":
    listener = Listener()
    listener.start_consume()
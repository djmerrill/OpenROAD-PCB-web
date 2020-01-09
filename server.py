"""
OpenROAD PCB Web job runner.

Usage:
  pcb-web.py
"""

import os
import time
from uuid import uuid4 as uuid
import datetime

from google.cloud import pubsub
from google.cloud import datastore
from docopt import docopt



def main(arguments):
    print(arguments)

    topic = 'OpenROAD-build-jobs'
    project_id = 'OpenROAD-PCB-web'
    subscription = 'OpenROAD-build-jobs'

    subscriber = pubsub.SubscriberClient()
    sub_path = subscriber.subscription_path(project_id, subscription)
    topic_path = subscriber.topic_path(project_id, topic)

    subscription_path = subscriber.subscription_path(project_id, subscription)
    print(topic_path)
    print(subscription_path)
    response = subscriber.pull(subscription_path, max_messages=1)

    for msg in response.received_messages:
        print("Received message:", msg.message.data)
    
    ack_ids = [msg.ack_id for msg in response.received_messages]
    subscriber.acknowledge(subscription_path, ack_ids)

    if len(response.received_messages) == 1:



if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    main(arguments)

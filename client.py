"""
OpenROAD PCB Web.

Usage:
  pcb-web.py (KICAD_FILE)
"""

import os
import time
from uuid import uuid4 as uuid
import datetime

from google.cloud import pubsub_v1
from google.cloud import datastore
from docopt import docopt



def main(arguments):
    print(arguments)

    job_id = str(uuid())


    client = datastore.Client()
    kind = 'BuildJob'
    name = job_id
    key = client.key(kind, name)
    job = datastore.Entity(
        key=key,
        exclude_from_indexes=['kicad_pcb']
    )

    
    with open(arguments['KICAD_FILE'], 'r') as f:
        job['kicad_pcb'] = f.read()
    job['created'] = datetime.datetime.utcnow()

    client.put(job)

    time.sleep(1)

    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        #project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        project_id='OpenROAD-PCB-web',
        topic='OpenROAD-build-jobs',  # Set this to something appropriate.
    )
    #publisher.create_topic(topic_name)
    publisher.publish(topic_name, b'build job for ' + arguments['KICAD_FILE'].encode(), uuid=job_id)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    main(arguments)

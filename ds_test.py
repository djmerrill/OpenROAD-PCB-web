
# Imports the Google Cloud client library
from google.cloud import datastore

# Instantiates a client
client = datastore.Client()

# The kind for the new entity
kind = 'Task'
# The name/ID for the new entity
name = 'sampletask1'
# The Cloud Datastore key for the new entity
task_key = client.key(kind, name)

# Prepares the new entity
task = datastore.Entity(key=task_key)
task['description'] = 'Buy milk'

# Saves the entity
client.put(task)

print('Saved {}: {}'.format(task.key.name, task['description']))


task = datastore.Entity(client.key('Task', 'learn'))
task.update({
    'category': 'Personal',
    'done': False,
    'priority': 4,
    'description': 'Learn Cloud Datastore'
})

client.put(task)

key = client.key('Task', 'sampletask1')
task = client.get(key)
print(task)

key = client.key('Task', 'learn')
task = client.get(key)
print(task)

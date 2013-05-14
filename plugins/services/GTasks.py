"""Module implementing the communication with the Google Tasks service.

"""

from tasks import Task, TaskList
import properties

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run


FLOW = OAuth2WebServerFlow(
    client_id=properties.GTASKS_AUTH_CLIENT_ID,
    client_secret=properties.GTASKS_AUTH_CLIENT_SECRET,
    scope=properties.GTASKS_AUTH_SCOPE,
    user_agent='synctasks/1.0')

gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')

storage = Storage('tasks.dat')

credentials = storage.get()

if credentials is None or credentials.invalid == True:
	credentials = run(FLOW, storage)

http = httplib2.Http()
http = credentials.authorize(http)

service = build(serviceName='tasks', version='v1', http=http,
       developerKey='AIzaSyDUHmvKfYda_ow9RGn7pOKDOllC45rnKJo')

def getTaskLists():
	"""
	Obtains all the user's task lists from the service.
	Returns a list of TaskList objects
	"""

	serverTasklists = service.tasklists().list().execute()

	taskLists = []

	for sTasklist in serverTasklists['items']:
		tasklist = TaskList.TaskList(sTasklist['title'])
		tasks = service.tasks().list(tasklist=sTasklist['id']).execute()
		for sTask in tasks['items']:
			task = Task.Task(
					sTask['title'],
					None,#sTask['parent'],
					2, #sTask['position'],
					''#sTask['notes']
			)
			#TODO: Change 'position' argument to deepnessLevel (calculate it)
			tasklist.append(task)
		taskLists.append(tasklist)
	
	return taskLists

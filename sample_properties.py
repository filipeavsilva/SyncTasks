"""
This is a properties file for the SyncTask script.

This file simply includes variables with assigned values.
Importing this module allows access to the variables as simple properties of the application (accessing properties.variable)
"""

#Google Tasks -specific properties
GTASKS_KIND_TASKLIST = 'tasks#tasks'
GTASKS_KIND_TASK = 'tasks#task'

GTASKS_TASKSTATUS_NEEDSACTION = 'needsAction'
GTASKS_TASKSTATUS_COMPLETED = 'completed'

GTASKS_AUTH_CLIENT_ID = ''
GTASKS_AUTH_CLIENT_SECRET = ''
GTASKS_AUTH_REDIRECT_URIS = ['urn:ietf:wg:oauth:2.0:oob', 'http://localhost']
GTASKS_AUTH_SCOPE = 'https://www.googleapis.com/auth/tasks'

#Taskpaper-specific properties
TASKPAPER_ISPROJECT_ATTR = ':TP_ISPROJECT:'

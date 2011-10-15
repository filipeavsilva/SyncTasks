import properties

class TaskList:
	"""Represents a Task List, as defined in the Google Tasks API.

	A Task list contains tasks."""

	def __init__(self, title):
		self.kind = properties.GTASKS_KIND_TASKLIST
		self.title = title
		self.etag = ''
		self.nextPageToken = ''
		self.items = []

	def __str__(self):
		result = 'Tasks:\n'
		for task in self.items:
			result += ' ' + str(task) + ',\n'
		result = result[:-1] #Remove the last comma
		return result

	def append(self, task):
		self.items.append(task)
	

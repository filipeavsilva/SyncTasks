import properties

class TaskAttribute:
	"""Represents a Task Attribute, be it a tag, a due date, a star..."""
	def __init__(self, key, value):
		self.key = key
		self.value = value


class Task:
	"""Represents a Task item, as specified by the Google Tasks API"""

	def __init__(self, title, parent, deepness, notes):
		self.kind = properties.GTASKS_KIND_TASK
		self.id = ""
		self.etag = ""
		self.title = title
		self.updated = None
		self.selfLink = None
		self.parent = parent
		self.deepnessLevel = deepness
		self.notes = notes
		self.status = properties.GTASKS_TASKSTATUS_NEEDSACTION
		self.due = None
		self.completed = None
		self.deleted = False
		self.hidden = False
		self.attributes = [] #List of TaskAttribute


	def __str__(self):
		result = self.title
		
		if self.notes is not None:
			result += ' [' + self.notes + ']'

		if self.completed is not None:
			result += ' (Completed)'

		return result

	def addAttribute(self, key, value):
		"""Adds an atribute to the attribute list"""

		self.attributes.append(TaskAttribute(key, value))

	def addAttributeList(self, attrList):
		"""Adds a whole list of attributes to the task's attribute list.

			Expects a list of two-element lists, in the form [key, value]

			e.g. [[key1, value1], [key2, value2], [key3, value3]]
		"""
		for kvPair in attrList:
			self.attributes.append(TaskAttribute(attrList[0], attrList[1]))


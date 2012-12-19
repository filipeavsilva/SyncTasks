import enums

TaskStatus = enums.enum(OPEN = 'Open',
		                    COMPLETED = 'Completed',
												CANCELED = 'Canceled',
												OVERDUE = 'Overdue')

class TaskAttribute:
	"""Represents a Task Attribute, be it a tag, a due date, a star..."""
	def __init__(self, key, value):
		self.key = key
		self.value = value


class Task:
	"""Represents a service- or filetype- independent Task"""

	def __init__(self, text, notes, parent=None):
		self.id = ""
		self.text = text
		self.selfLink = None
		self.notes = notes
		self.due = None
		self.status = TaskStatus.OPEN
		self.attributes = [] #List of TaskAttribute
		self.parent = parent #Parent task
		self.children = [] #List of children Tasks


	def __str__(self):
		result = self.text
		
		if self.notes is not None:
			result += ' [{0}]'.format(self.notes)

		if self.status is not None:
			result += ' ({0})'.format(str(self.status))

		if self.children is not None and len(self.children) > 0:
			result += ' ({0} children)'.format(len(self.children))

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


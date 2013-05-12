from lib.enums import enum
import properties

class TaskAttribute:
	"""Represents a Task Attribute, be it a tag, a star, etc."""
	def __init__(self, key, value):
		self.key = key
		self.value = value


class Task:
	"""Represents a single task"""

	def __init__(self, title, parent, notes):
		self.title = title
		self.updated = None
		self.parent = parent
		self.children = []
		self.notes = notes
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

	def add_attribute(self, key, value):
		"""Adds an atribute to the attribute list"""

		self.attributes.append(TaskAttribute(key, value))

	def add_attribute_list(self, attrList):
		"""Adds a whole list of attributes to the task's attribute list.

			Expects a list of two-element lists, in the form [key, value]

			e.g. [[key1, value1], [key2, value2], [key3, value3]]
		"""
		for kvPair in attrList:
			self.attributes.append(TaskAttribute(kvPair[0], kvPair[1]))

	def add_child(self, task):
		""" Adds a child task, if it doesn't already have a parent """

		if task.parent is None:
			task.parent = self
			self.children.append(task)
		else:
			raise Exception("Task already has a parent")

class TaskList:
	"""Represents a Task List, as defined in the Google Tasks API.

	A Task list contains tasks."""

	def __init__(self, title):
		self.title = title
		self.items = []

	def __str__(self):
		result = 'Tasks:\n'
		for task in self.items:
			result += ' ' + str(task) + ',\n'
		result = result[:-1] #Remove the last comma
		return result

	def append(self, task):
		self.items.append(task)

from lib.enums import enum
import properties

class Task:
	"""Represents a single task"""

	def __init__(self, title, notes = None, parent = None):

		if title is None:
			raise ValueError("Task cannot be created without a Title")

		self.title = title
		self.children = []
		self.notes = notes
		self.complete = False
		self.virtual = False
		self.attributes = {}

		self.parent = None
		if parent is not None:
			parent.add_child(self)


	def __str__(self):
		result = self.title
		
		if self.notes is not None:
			result += ' [' + self.notes + ']'

		if self.complete is not None:
			result += ' (Completed)'

		return result

	@classmethod
	def create_virtual_task(cls, title = None):
		"""Creates a virtual task, i.e. a task that serves only as the root of a tree or list of tasks"""

		t = Task('')
		t.title = title
		t.virtual = True

		return t


	def add_attribute(self, key, value):
		"""Adds an atribute to the attribute list"""

		if self.virtual:
			raise Exception("Virtual tasks cannot have attributes")

		if key in self.attributes:
			raise KeyError("Attribute {0} already exists".format(key))

		self.attributes[key] = value

	def add_attribute_list(self, attrList):
		"""Adds a whole list of attributes to the task's attribute list.

			Expects a list of two-element lists, in the form [key, value]

			e.g. [[key1, value1], [key2, value2], [key3, value3]]
		"""
		for kvPair in attrList:
			self.add_attribute(kvPair[0], kvPair[1])


	def add_child(self, task):
		""" Adds a child task, if it doesn't already have a parent """

		if not task.virtual:
			if task.parent is None:
				task.parent = self
				self.children.append(task)
			else:
				raise Exception("Task already has a parent")
		else:
			raise Exception("Virtual tasks cannot have parents")

	
	def add_children(self, children):
		"""Adds a list of children at once"""

		for child in children:
			self.add_child(child)

import enums

TaskStatus = enums.enum(OPEN = 'Open',
		                    COMPLETED = 'Completed',
												CANCELED = 'Canceled',
												OVERDUE = 'Overdue')


class Task:
	"""Represents a service- or filetype- independent Task"""

	def __init__(self, text='', notes='', parent=None):
		self.id = ""
		self.text = text
		self.selfLink = None
		self.notes = notes
		self.due = None
		self.status = TaskStatus.OPEN
		self.attributes = {}
		self.children = [] #List of children Tasks
		self.parent = None #Initialize the parent task as None
		if parent is not None and isinstance(parent, self.__class__): #Parent is not None and it's a Task
			parent.addChild(self) #Set this task as its parent's child


	def __str__(self):

		return 'Task{{Text: "{0}", Notes: "{1}", Attributes: "{2}", Children: "{3}"}}'.format(self.text if self.text is not None else "''",
				self.notes if self.notes is not None else "''", self.attributes, len(self.children))

		#result = '=> '
		#result += self.text
		
		#if self.notes is not None:
			#result += ' [{0}]'.format(self.notes)

		##if self.status is not None:
			##result += ' ({0})'.format(str(self.status))

		#if self.children is not None and len(self.children) > 0:
			#result += ' ({0} children)'.format(len(self.children))

		#for child in self.children:
			#result += '\n\t{0}'.format(str(child))

		return result

	def setAttribute(self, key, value=True):
		"""Set the value of an attribute"""

		self.attributes[key] = value

	def getAttribute(self, key):
		"""Get the value of an attribute. Return None if the key does not exist."""

		try:
			return self.attributes[key]
		except KeyError:
			return None

	def addChild(self, childTask):
		"""Adds a task as a child of this one."""
		if childTask is not None:
			self.children.append(childTask)
			childTask.parent = self

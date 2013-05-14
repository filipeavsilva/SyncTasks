from testify import *
from tasks import *

class TasksTestCase(TestCase):
	"""Tests for task's and tasklist's creation and simple operations"""

	@class_setup
	def init_vars(self):
		self.title = 'A TITLE'
		self.notes = 'SOME NOTES'
		self.attr_key = 'key'
		self.attr_value = 'value'


	def test_create_task(self):
		"""Test creating a task without a parent"""

		task = Task(self.title, self.notes)

		assert_equal(task.title, self.title)
		assert_equal(task.notes, self.notes)
		assert_equal(task.complete, False)
		assert_equal(task.virtual, False)
		assert_equals(task.children, [])
		assert_equals(task.attributes, {})


	def test_create_task(self):
		"""Test creating a task without notes"""

		task = Task(self.title)

		assert_equal(task.title, self.title)
		assert_equal(task.notes, None)
		assert_equal(task.complete, False)
		assert_equal(task.virtual, False)
		assert_equals(task.children, [])
		assert_equals(task.attributes, {})


	def test_create_task_no_title(self):
		"""Test creating a task without a title"""

		assert_raises(ValueError, Task, None)


	def test_create_task_with_parent(self):
		"""Test creating a task with a parent"""

		parent = Task(self.title, self.notes)

		child = Task(self.title, self.notes, parent)

		assert_equal(child.parent, parent)
		assert_equal(len(parent.children), 1)
		assert_equal(parent.children[0], child)


	def test_task_add_child(self):
		"""Test adding a child to a task"""

		parent = Task(self.title, self.notes)

		child = Task(self.title, self.notes)

		parent.add_child(child)

		assert_equal(child.parent, parent)
		assert_equal(len(parent.children), 1)
		assert_equal(parent.children[0], child)


	def test_task_two_parents(self):
		"""Test adding a second parent to a task"""

		parent = Task(self.title, self.notes)
		
		parent2 = Task(self.title, self.notes)

		child = Task(self.title, self.notes)

		parent.add_child(child)
		assert_raises(Exception, parent2.add_child, child)


	def test_task_add_multiple_children(self):
		"""Test adding multiple children at once to a task"""

		parent = Task(self.title, self.notes)
		
		child = Task(self.title, self.notes)
		child2 = Task(self.title, self.notes)
		child3 = Task(self.title, self.notes)

		parent.add_children([child, child2, child3])

		assert_equals(len(parent.children), 3)
		assert_equals(child.parent, parent)
		assert_equals(child2.parent, parent)
		assert_equals(child3.parent, parent)


	def test_create_virtual_task(self):
		"""Test creating a regular virtual task without a title"""

		virt = Task.create_virtual_task()

		assert_equals(virt.parent, None)
		assert_equals(virt.virtual, True)
		assert_equals(virt.title, None)
		assert_equals(virt.notes, None)
		assert_equal(virt.complete, False)
		assert_equals(virt.children, [])
		assert_equals(virt.attributes, {})


	def test_create_virtual_task_with_title(self):
		"""Test creating a regular virtual task with a title"""

		virt = Task.create_virtual_task(self.title)

		assert_equals(virt.parent, None)
		assert_equals(virt.virtual, True)
		assert_equals(virt.title, self.title)
		assert_equals(virt.notes, None)
		assert_equal(virt.complete, False)
		assert_equals(virt.children, [])
		assert_equals(virt.attributes, {})


	def test_virtual_task_add_children(self):
		"""Test adding children to a virtual task"""

		virt = Task.create_virtual_task()
		task = Task(self.title)

		virt.add_child(task)

		assert_equals(task.parent, virt)
		assert_equals(len(virt.children), 1)
		assert_equals(virt.children[0], task)

	
	def test_virtual_task_parent(self):
		"""Test adding a parent to a virtual task"""

		virt = Task.create_virtual_task()
		parent = Task(self.title)

		assert_raises(Exception, parent.add_child, virt)


	def test_adding_attribute(self):
		"""Test adding an attribute to a task"""

		task = Task(self.title)
		
		task.add_attribute(self.attr_key, self.attr_value)

		assert_equals(len(task.attributes), 1)
		assert_equals(task.attributes[self.attr_key], self.attr_value)


	def test_adding_multiple_attributes(self):
		"""Test adding multiple attributes to a task"""

		task = Task(self.title)
		
		task.add_attribute_list([[self.attr_key, self.attr_value],
			[self.attr_value, self.attr_key], [self.attr_key + '2',
				self.attr_value]])

		assert_equals(len(task.attributes), 3)
		assert_equals(task.attributes[self.attr_key], self.attr_value)
		assert_equals(task.attributes[self.attr_value], self.attr_key)
		assert_equals(task.attributes[self.attr_key + '2'], self.attr_value)
	

	def test_adding_attribute_to_virtual_task(self):
		"""Test adding an attribute to a virtual task"""

		virt = Task.create_virtual_task()
		
		assert_raises(Exception, virt.add_attribute, self.attr_key, self.attr_value)


	def test_adding_multiple_attributes_to_virtual_task(self):
		"""Test adding multiple attributes to a virtual task"""

		virt = Task.create_virtual_task()
		
		assert_raises(Exception, virt.add_attribute_list, [[self.attr_key,
			self.attr_value], [self.attr_value, self.attr_key], [self.attr_key + '2',
				self.attr_value]])

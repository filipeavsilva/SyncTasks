from tasks import Task

import os.path
import re
import codecs

#Constants for dictionary keys
TASK = 'task'
DEEP = 'depth'

TEXT = 'text'
TAGS = 'tags'


######################################################################################## Read file #
def readFile(path):
	"""	Reads a file from disk and parses it into tasks.	"""

	tasksFile = codecs.open(path, 'r', encoding='utf-8')
	tasklist = []
	currTask = None

	
	for line in tasksFile:
		thing = parseLine(line)

		if type(thing) in [str, unicode]: #It's a note
			if len(thing) > 0 and currTask is not None:
				currTask.notes += thing
			#else, do nothing

		elif isinstance(thing, Task):
			#If the newfound task is shallower than the current, climb the hierarchy
			# until a suitable parent is found (or add it to top level)
			while currTask is not None and thing.getAttribute('taskpaper-depth') <= currTask.getAttribute('taskpaper-depth'):
				currTask = currTask.parent

			if currTask is None:
				tasklist.append(thing) #Add to the top level
				currTask = thing
			else:
				currTask.addChild(thing) #Add as a child and proceed from here
				currTask = thing

	return tasklist

######################################################################################## Write file #
def writeFile(tasklist, path):
	"""Writes the task list to a taskpaper file"""

	def task2Str(task):
		""" Writes a single task into a string."""
		text = ''

		tabs = '\t' * task.getAttribute('taskpaper-depth')
		text += tabs

		if task.getAttribute('taskpaper-is-project') is not None:
			text += '{}:'.format(task.text)
		else:
			text += '- {}'.format(task.text)

		for tag in [(key.replace('tag-', ''), task.getAttribute(key)) for key in task.attributes if key.startswith('tag-')]:
			text += ' @{}{}'.format(tag[0], '('+tag[1]+')' if len(tag[1]) > 0 else '')

		if task.notes is not None and len(task.notes) > 0:
			text += '\n' + tabs + task.notes

		for child in task.children:
			text += '\n' + task2Str(child)

		return text

	fileText = ""
	for task in tasklist:
		fileText += task2Str(task) + '\n'

	file = codecs.open(path, 'w', encoding='utf-8') #Overwrites or creates the file
	file.write(fileText)
	file.close()





########################################################################## Auxilliary methods #

def last(lst):
	"""Helper function to return the last element of a list.
		 If the list is empty returns None. """
	if lst is not None and len(lst) > 0:
		return lst[-1]
	else:
		return None

def parseLine(txtLine):
	""" Parses a line of text. Returns a Task, or the line itself (string) if not a task. """
	DEPTH = 0
	TEXT_TASK = 1
	TEXT_PROJECT = 2
	TAGS_PROJECT = 3

	TAG_NAME = 0
	TAG_VALUE = 1

	taskRE = re.compile(r'(\t*)(?:(?:-\s(.+))|(?:(\S.+):([^:]*)))', re.UNICODE) #Matches tasks and projects
	tagsRE = re.compile(r'@([^(\s]+)(?:\(([^)]+)?\))?', re.UNICODE) #Matches a task's tags

	match = taskRE.search(txtLine)
	if match is not None: #It's a task
		match = match.groups()
		text = match[TEXT_TASK]
		
		if text is None or len(text) == 0: #Not a task, then it's a project
			text = match[TEXT_PROJECT] + (match[TAGS_PROJECT] if match[TAGS_PROJECT] is not None else '')
			is_project = True
		else:
			text = match[TEXT_TASK]
			is_project = False

		#Extract all the tags from the text
		tags = tagsRE.findall(text)
		text = tagsRE.sub('', text).strip()
		
		task = Task(text)
		task.setAttribute('taskpaper-depth', len(match[DEPTH])) #Keep the depth as an attribute
		if is_project:
			task.setAttribute('taskpaper-is-project')

		#Add all the tags as attributes to the task
		for tag in tags:
			task.setAttribute('tag-{0}'.format(tag[TAG_NAME]), tag[TAG_VALUE])
		return task
	else: #Not a task. Either empty or a task's note
		return txtLine.strip()


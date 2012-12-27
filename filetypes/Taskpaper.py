from tasks import Task, TaskAttribute

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

		if type(thing) == 'str': #It's a note
			if currTask is not None:
				currTask.notes += thing
			#else, do nothing

		elif isinstance(thing, Task):
			#If the newfound task is shallower than the current, climb the hierarchy
			# until a suitable parent is found (or add it to top level)
			while currTask is not None and thing.depth <= currTask.depth:
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
	fileText = getFileString(tasklist)

	file = codecs.open(path, 'w', encoding='utf-8') #Overwrites or creates the file
	file.write(fileText)
	file.close()



################################################################################# Auxilliary methods #

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
	TEXT = 1
	TAGS = 2
	TAG_NAME = 0
	TAG_VALUE = 2

	taskRE = re.compile(r'(\t*)-(\s.*)|(.*):', re.UNICODE) #Matches tasks and projects
	taskDepthRE = re.compile(r'\s')
	tagsRE = re.compile(r'@\S+', re.UNICODE) #Matches a task's tags
	tagPartsRE = re.compile(r'@([^(]+)(\(([^)]+)\))?')

	matches = taskRE.findall(txtLine)
	if matches != []: #It's a task
		match = matches[0]
		task = Task(match[TEXT])
		task.depth = 	max(1, len(taskDepthRE.findall(match[DEPTH])))
		#Add all the tags as attributes to the task
		for tag in tagsRE.findall(match[TAGS]):
			tagParts = tagPartsRE.findall(tag)[0]
			task.addAttribute('tag-{0}'.format(tagParts[TAG_NAME]), tagParts[TAG_VALUE])
		return task
	else: #Not a task. Either empty or a task's note
		return txtLine.strip()


#TODO: Upgrade this crap
def getFileString(tasklist):
	"""Serializes a task list to a list in the taskpaper format"""
	fileText = ""

	for task in tasklist:
		#isProject = False
		#taskLine = ""

		#depthTabs = "\t"*(task.depthLevel)
		#taskLine += task.title
		
		#for attr in task.attributes:
			#if attr.key == properties.TASKPAPER_ISPROJECT_ATTR:
				#isProject = True
			#else:
				#taskLine += " @" + attr.key
				#if (attr.value is not None and attr.value != ""):
					#taskLine += "("+attr.value+")"
		
		#if isProject:
			#taskLine = "\n" + taskLine + ":"
		#else:
			#taskLine = "- " + taskLine

		#taskLine = depthTabs + taskLine

		#taskLine += "\n" + task.notes.replace("\n", "\n"+("\t"*task.depthLevel)) #Indent notes
		#fileText += taskLine
	return fileText

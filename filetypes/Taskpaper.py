from tasks import Task, TaskList
import properties

import os.path
import re
import codecs

#Constants for dictionary keys
TASK = 'task'
DEEP = 'deepness'

TITLE = 'title'
TAGS = 'tags'

def parseTask(txtLine):
	""" Takes a line of text representing a task and returns all its constituents """
	taskParts = {}
	tagList = re.findall(r'@\S+', txtLine, re.UNICODE) #finds all the tags, including value parameters
	tagsAndValues = []

	for tagStr in tagList:
		tagBody = re.findall('@([^(]+)')[0]
		tagValue = re.findall('\(([^)]+)\)')[0]

		tagsAndValues.append([tagBody, tagValue])

	taskParts[TITLE] = txtLine[:-1] #Remove newline
	taskParts[TAGS] = tagsAndValues

	return taskParts


def getLast(lst):
	"""Helper function to return the last element of a list.
		 If the list is empty returns None. """
	if len(lst) > 0:
		return lst[-1]
	else:
		return None

def readFile(path):
	"""Reads a file from disk and parses it into a task list."""

	tasksFile = open(path, 'r')
	tasklist = TaskList.TaskList(os.path.splitext(os.path.basename(path))[0])
	parentStack = [] #Initialize the stack of parent tasks

	task = None

	for line in tasksFile:
		deepness = 1
		line = line.rstrip() #Remove the trailing whitespaces (newlines, mainly)

		while line.startswith("\t"): #starts with tab
			deepness += 1		#Add a deepness level to the current line
			line = line[1:] #Remove the leading tab

		if line.startswith("- ") or line.endswith(':'): #It's a task or a project (both are saved as tasks)
			if task is not None:		#There's a previous task	
				tasklist.append(task) #Commit previous task to the list

			if (getLast(parentStack) is None and deepness > 1) or	deepness > getLast(parentStack)[DEEP]:
						parentStack.append({TASK:task, DEEP:deepness}) #This'll be parent to the next ones
			else:
				if deepness < getLast(parentStack)[DEEP]:
					parentStack.pop() #Up one level

			#Get the new task's parent from the stack
			parent = getLast(parentStack)
			if parent is not None:
				parent = parent[0]

			#Create the task object
			if line.startswith("- "): #It's a regular task
				taskParts = parseTask(line[2:])
				task = Task.Task(taskParts[TITLE], parent, deepness, '')
				task.addAttributeList(taskParts[TAGS])
			else:	#It's a project
				task = Task(line[:-1], parent, deepness, '') #Remove ':' from the task title
				task.addAttribute(properties.TASKPAPER_ISPROJECT_ATTR, '') #Mark it as a project

		else:
			if task is not None: 
				task.notes += line

	#Put last task in the list
	if task is not None:
		tasklist.append(task)


	return tasklist

def getFileString(tasklist):
	"""Serializes a tasklist to a list in the taskpaper format"""
	fileText = ""

	for task in tasklist.items:
		isProject = False
		taskLine = ""

		deepnessTabs = "\t"*(task.deepnessLevel)
		taskLine += task.title
		
		for attr in task.attributes:
			if attr.key == properties.TASKPAPER_ISPROJECT_ATTR:
				isProject = True
			else:
				taskLine += " @" + attr.key
				if (attr.value is not None and attr.value != ""):
					taskLine += "("+attr.value+")"
		
		if isProject:
			taskLine = "\n" + taskLine + ":"
		else:
			taskLine = "- " + taskLine

		taskLine = deepnessTabs + taskLine

		taskLine += "\n" + task.notes.replace("\n", "\n"+("\t"*task.deepnessLevel)) #Indent notes
		fileText += taskLine
	return fileText

def writeFile(tasklist, path):
	"""Writes the task list to a taskpaper file"""
	fileText = getFileString(tasklist)

	file = codecs.open(path, 'w', encoding='utf-8') #Overwrites or creates the file
	file.write(fileText)
	file.close()


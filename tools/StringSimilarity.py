"""
	Module StringSimilarity

	Provides functions to compute a similarity measure between sets of strings

	Adapted from Java code in http://www.catalysoft.com/articles/StrikeAMatch.html?article=How_to_Strike_a_Match_15

	Credit for the algorithm goes to Simon White
"""
import re

def __init__():
	pass

def letterPairs(str):
	"""
		Returns a list of adjacent letter pairs contained in the input string
	"""
	str = re.sub("\\W", "", str, 0, re.UNICODE) #Remove non-alphanumeric characters
	numPairs = len(str)-1
	pairs = []

	for i in range(numPairs):
		pairs.append(str[i:i+2])
	
	return pairs

def wordLetterPairs(str):
	"""
		Returns all the adjacent 2-character pairs present in the string
		(ignoring whitespace and non-alphanumeric characters)
	"""
	words = re.split("\\s", str)
	allPairs = []

	for word in words:
		allPairs.extend(letterPairs(word)) #gradually gathers all character pairs in this string

	return allPairs

def compareStrings(str1, str2):
	"""
		Compares two strings and returns a similarity measure in the range [0, 1]
	"""
	pairs1 = wordLetterPairs(unicode(str1.upper()))
	pairs2 = wordLetterPairs(unicode(str2.upper()))
	intersection = 0
	union = len(pairs1) + len(pairs2)

	for i in range(len(pairs1)):
		pair1 = pairs1[i]

		for j in range(len(pairs2)):
			pair2 = pairs2[j]

			if pair1 == pair2:
				intersection += 1
				pairs2.pop(j)
				break
	
	return (2.0 * intersection)/union

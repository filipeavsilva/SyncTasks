import sys
import argparse
import re
import alpha_luhn

def base10toN(num,n):
	"""Change a to a base-n number.
	Up to base-36 is supported without special notation."""
	num_rep={10:'A',
				11:'B',
				12:'C',
				13:'D',
				14:'E',
				15:'F',
				16:'G',
				17:'H',
				18:'I',
				19:'J',
				20:'K',
				21:'L',
				22:'M',
				23:'N',
				24:'O',
				25:'P',
				26:'Q',
				27:'R',
				28:'S',
				29:'T',
				30:'U',
				31:'V',
				32:'W',
				33:'X',
				34:'Y',
				35:'Z'}
	new_num_string=''
	current=num
	while current!=0:
		remainder = current % n
		if 36>remainder>9:
			remainder_string=num_rep[remainder]
		elif remainder>=36:
			remainder_string='('+str(remainder)+')'
		else:
			remainder_string=str(remainder)
		new_num_string=remainder_string+new_num_string
		current=current/n
	return new_num_string

def generate_alphaseq(start, iterations, string, symbol, filename, silent, forbidden, check_digit):
	#Handle the case where the string is empty
	if len(string) == 0:
		if len(symbol) == 0:
			symbol = '%'
		string = symbol

	iStart = int(start)
	i = int(iStart)
	end = i + int(iterations) - 1
	strToFile = ''
	while i <= end:
		ib = base10toN(i, 36)
		num = ib
		if check_digit:
			num = num + str(alpha_luhn.return_checkdigit(ib))

		#Check if the number is in the forbidden word list
		good = True
		for regex in forbidden:
			if regex.match(num):
				good = False
				break

		if good:
			if not silent:
				print(string.replace(symbol, num)) #Prints the generated number

			strToFile += num + '\n'
		else:
			#If the generated number is not acceptable, add 1 to the end var to assure the requested amount of numbers is generated
			end += 1

		i += 1
	
	if filename != '':
		try:
			listFile = open(filename, 'w')
			listFile.write(strToFile)
			listFile.close()
		except:
			sys.stderr.write('Error when writing to file \'' + filename + '\'')

#Main
if __name__ == '__main__':
	#Argument parser
	parser = argparse.ArgumentParser(description='Generates a list of sequential alphanumeric strings')

	parser.add_argument('start_number', help='The starting number (alphanumeric) of the sequence. If --convert is specified, this parameter is used as the number to convert.')
	parser.add_argument('iterations', help='The (integer) number of iterations to include in the list.', nargs='?', default=-1, type=int)

	parser.add_argument('-s', '--string', help='String where each of the generated numbers will be included.', default='')
	parser.add_argument('-r', '--symbol-replace', help='Substring which will be replaced, in the string, for the generated numbers.', default='')
	parser.add_argument('-o', '--output', help='Name of the file to which the list of generated numbers will be written. If empty, the list will only be output to the screen. If empty and --silent is specified, the script exits with an error.', default='')
	parser.add_argument('-sl', '--silent', help='If specified, the generated numbers will not be printed to the screen. If specified and --output is not specified, the script exits with an error.', action='store_true')
	parser.add_argument('-x', '--excluded-words', help='Word (or list of words, separated by commas (",") ) to exclude from the output. Wildcards "?" and "*" may be used to specify ranges of words.', default='')
	parser.add_argument('-xf', '--excluded-word-file', help='Name of a file containing a list of words (one per line) to exclude from the output. Wildcards "?" and "*" may be used to specify ranges of words.', default='')
	parser.add_argument('-c', '--convert', help='Prints the alphanumeric equivalent of the number inserted as start_number (effectively converts it to base 36. Useful for testing)', action='store_true')
	parser.add_argument('-cd', '--check-digit', help='If specified, the generated numbers will have a check digit appended to them.', action='store_true')
	

	args = parser.parse_args()

	if args.silent and args.list_filename == '':
		print('Error: If silent mode is enabled, a filename must be specified.')
	else:
		if args.convert: #Just convert the number
			num = base10toN(int(args.start_number), 36)
			if args.check_digit:
				num = num + str(alpha_luhn.return_checkdigit(num))
			print(num)
		else:
			if args.iterations == -1:
				print('Error: If --convert is not specified, a number of iterations must be inserted.')
			nonoes = []

			if args.excluded_words != '':
				for word in args.excluded_words.split(','):
					if word.strip() != '':
						nonoes.append(re.compile('.*' + word.strip().upper().replace('*', '[A-Z0-9]*').replace('?', '[A-Z0-9]?') + '.*'))

			if args.excluded_word_file != '':
				try:
					fnono = open(args.excluded_word_file, 'r')
					for line in fnono:
						nonoes.append(re.compile('.*' + line.strip().upper().replace('*', '[A-Z0-9]*').replace('?', '[A-Z0-9]?') + '.*'))
				except:
					print('ERROR!!!')
					pass

			generate_alphaseq(args.start_number, args.iterations, args.string, args.symbol_replace, args.output, args.silent, nonoes, args.check_digit)

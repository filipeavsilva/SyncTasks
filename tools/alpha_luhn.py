import math
def return_checkdigit(id_without_check):
	# allowable characters within identifier
	valid_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVYWXZ_"

	# remove leading or trailing whitespace, convert to uppercase
	id_without_checkdigit = id_without_check.strip().upper()

	# this will be a running total
	sum = 0;

	# loop through digits from right to left
	for n, char in enumerate(reversed(id_without_checkdigit)):

		if not valid_chars.count(char):
			raise Exception('InvalidIDException')

		# our "digit" is calculated using ASCII value - 48
		digit = ord(char) - 48

		# weight will be the current digit's contribution to
		# the running total
		weight = None
		if (n % 2 == 0):
			#for alternating digits starting with the rightmost, we
			#use our formula this is the same as multiplying x 2 and
			#adding digits together for values 0 to 9. Using the
			#following formula allows us to gracefully calculate a
			#weight for non-numeric "digits" as well (from their
			#ASCII value - 48).
			weight = (2 * digit) - (digit / 5) * 9
		else:
			# even-positioned digits just contribute their ascii
			# value minus 48
			weight = digit

		# keep a running total of weights
		sum += weight

	#End FOR
	# avoid sum less than 10 (if characters below "0" allowed,
	# this could happen)
	sum = math.fabs(sum) + 10

	# check digit is amount needed to reach next number
	# divisible by ten. Return an integer
	return int((10 - (sum % 10)) % 10)

"""
Module implementing the Luhn's Algorithm for check digit calculation and verification.

Code obtained from http://en.wikipedia.org/wiki/Luhn_algorithm
"""

def __init__():
	pass

def calculate(number):
	"""Calculates the check digit for a number"""
	num = map(int, str(number))
	check_digit = 10 - sum(num[-2::-2] + [sum(divmod(d * 2, 10)) for d in num[::-2]]) % 10
	return 0 if check_digit == 10 else check_digit

def verify(number):
	"""Verifies if a number is correct anumberording to its check digit"""
	num = map(int, str(number))
	return sum(num[::-2] + [sum(divmod(d * 2, 10)) for d in num[-2::-2]]) % 10 == 0

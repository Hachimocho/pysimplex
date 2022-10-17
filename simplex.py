# Authors: Aidan Lynch, Bryce Gernon, Jim Godin, Ryan Devoe, Sam Ford
from ctypes import Union
import sys
from typing import Tuple  # Command line argument handling
import numpy  # Python matrix ops
from fractions import Fraction
import os  # Could be useful for saving output to file if desired

import numpy as np

'''
 * Class for storing the result of parsing command line arguments
 *
 * success: parsing of command line arguments was successful
 * m: number of rows
 * n: number of columns
 '''


class ArgResult:

	def __init__(self):
		self.m = -1
		self.n = -1
		self.success = False


'''
 * class for storing the result the payoff matrix entry
 *
 * success: entry of payoff matrix was successful
 * payoff: payoff matrix
 * m: number of rows
 * n: number of columns
 '''


class PayoffResult:

	def __init__(self, m, n):  # Equivalent to get_payoff
		self.success = False
		self.payoff = []
		self.m = 0
		self.n = 0

	'''
    * Sets a PayoffResult object to nothing
    *
    * result: payoff result structure
    '''

	def free_payoff_result(self):
		free_2d_arr(self.payoff, self.m)
		self.n = -1
		return


'''
 * Class to store a pivot result
 *
 * success: if the pivot was successful
 * tableau: tableau resulting from pivot\
 * pivot_row: row of the pivot used
 * pivot_col: col of the pivot used
 '''


def format_frac(frac):
	if frac.numerator == 0:
		return "0"
	elif frac.denominator == 1:
		return "{}".format(frac.numerator)
	else:
		return "{}/{}".format(frac.numerator, frac.denominator)

'''
 * Struct for storing a tableau
 *
 * m: matrix
 * s_size: length of S
 * x_size: length of X
 * rows: number of rows in m
 * cols: number of columns in m
 '''


class Tableau:
	# this is equivalent to create_tableau in Aidan's simplex.c
	def __init__(self, s_size, x_size):
		self.s_size = s_size
		self.x_size = x_size
		self.rows = s_size + 1
		self.cols = x_size + s_size + 1
		self.k = 0
		# print( self.rows, self.cols, "in tableau constructor")
		# numpy makes 2 for loops in C into a line of code - SF 10/13
		self.m = numpy.zeros((self.rows, self.cols)).astype('object')  # Generate m here
		for row, _ in enumerate(self.m):
			for col, _ in enumerate(self.m[row]):
				self.m[row][col] = Fraction(0)

	# equivalent to print_tableau in Aidan's simplex.c
	def __str__(self):
		tableau_str = ""
		for row in range(self.rows):
			if row == self.s_size:
				tableau_str += "-" * (8 * self.cols + 2) + "\n"
			for col in range(self.cols):
				if col == self.x_size or col == self.x_size + self.s_size:
					tableau_str += "|"

				frac = Fraction(self.m[row][col])
				tableau_str += "{:^8}".format(format_frac(frac))
			if row < self.rows - 1:
				tableau_str += "\n"
		return tableau_str

	'''
    * Sets tableau object as non-usable
    *
    * tableau: struct to free
    * 
    '''

	def free_tableau(self):
		free_2d_arr(self.m, self.rows)
		self.s_size = -1
		self.x_size = -1
		self.cols = -1
		self.k = -1
		return


''''set the 2d arr to nothing'''


def free_2d_arr(arr, rows):
	arr = None
	rows = -1
	return


'''
 * Print the usage statement for this program.
 '''


def print_usage():
	print("usage: simplex m n\n")
	print("\tm: number of rows, integer greater than 0\n")
	print("\tn: number of columns, integer greater than 0\n")


'''
 * Parses this program's command line arguments.
 *
 * argc: number of command line arguments
 * argv: array of string tokens
 *
 * return: arg result structure
 '''


def parse_args(argc: int, argv: list) -> ArgResult:
	result = ArgResult()

	# do we want to prompt for input if
	# rows and cols not provided? - SF 10/13
	if (argc != 3):
		result.m = -1
		result.n = -1
		return result

	# parse row and column numbers
	try:
		m: int = int(argv[1])
		assert m > 0
		n: int = int(argv[2])
		assert n > 0
	except Exception:
		result.m = -1
		result.n = -1
		return result

	result.m = m
	result.n = n
	result.success = True
	return result


'''
 * Prompt user for payoff matrix and process its entry.
 *
 * m: number of rows
 * n: number of columns
 *
 * return: payoff result structure
 '''


def get_payoff(m: int, n: int) -> PayoffResult:
	result = PayoffResult(m, n)
	# initialize a mxn numpy array
	result.payoff = numpy.zeros((m, n))
	result.m = m
	result.n = n

	# string interpolation
	print(f"Please enter the {m} by {n} payoff matrix below."
	      "\nSeparate rows by new lines and columns by spaces: \n")

	mat_str: str = ""
	row_els: list = []
	r_count: int = -1
	lineNum = 0
	while lineNum < m:
		mat_str = input()
		row_els = mat_str.split()
		r_count = len(row_els)

		if (r_count != n):
			print(f"Expected {n} entries in a row. Got {r_count} Aborting.")
			result.success = False
			return result

		# validate the input we got was numbers
		for col in range(0, n):
			try:
				num = Fraction(row_els[col])
				result.payoff[lineNum][col] = num
			except ValueError:
				print("Couldn't convert input string to fraction")
				result.success = False
				free_2d_arr(result.payoff, m)
				return result
		# endfor
		lineNum += 1
	# endwhile
	result.success = True
	return result


'''
 * Builds the initial tableau using the given payoff matrix
 *
 * payoff: payoff matrix
 * m: number of rows
 * n: number of columns
 *
 * return: initial tableau
 '''


def get_init_tableau(payoff, m, n) -> Tableau:
	tableau: Tableau = Tableau(m, n)

	min = sys.maxsize
	for row in range(0, m):
		for col in range(0, n):
			if (payoff[row][col] < min):
				min = payoff[row][col]

	# Python ternary assignment of booster val k
	k = Fraction(1 - min) if (min < 1) else Fraction(0)

	# populate the initial tableau so that every entry >=
	# in the elif the == will eval to 1 or 0 since
	# True or False is equiv to those respectively
	for row in range(0, m):
		for col in range(0, n):
			if (col < n):
				tableau.m[row][col] = Fraction(payoff[row][col] + k) \
					if (row < m) else Fraction(-1)
			elif (col < n + m):
				tableau.m[row][col] = Fraction((row == col - n)) \
					if (row < m) else Fraction(0)
			else:
				tableau.m[row][col] = Fraction((row < m))

	# Add default values to tableau
	for x in range(m):
		tableau.m[n][x] = -1
		tableau.m[x][m+n] = 1
		tableau.m[x][n+x] = 1

	return tableau


'''
 * Pivots the provided tableau
 *
 * tableau: struct to pivot
 '''


def pivot_tableau(tableau: Tableau) -> Tuple[Tableau, int, int]:
	pivot_col = np.argmin(tableau.m[tableau.rows-1])
	min_value = sys.maxsize
	pivot_row = Fraction(-1)
	for row, entry in enumerate(np.swapaxes(tableau.m, 0, 1)[pivot_col][0:-1]):
		value = Fraction(1 / entry)
		if 0 < value < min_value:
			min_value = value
			pivot_row = row
	pivot_value = Fraction(tableau.m[pivot_row][pivot_col])
	prev_tableau = np.copy(tableau.m)
	for col, _ in enumerate(tableau.m[pivot_row]):
		tableau.m[pivot_row][col] = Fraction(tableau.m[pivot_row][col] / pivot_value)

	for row, _ in enumerate(tableau.m):
		for col, _ in enumerate(tableau.m[row]):
			if row != pivot_row:
				tableau.m[row][col] = Fraction(tableau.m[row][col] - Fraction(prev_tableau[row][pivot_col] * tableau.m[pivot_row][col]))

	return (tableau, pivot_row, pivot_col)


'''
 * Runs the simplex method on the supplied payoff matrix.
 *
 * argc: number of command line arguments
 * argv: array of tokens
 *
 * return: 0 on successful execution
 '''


def main():
	# Parse inputs
	parse_result: ArgResult = parse_args(len(sys.argv), sys.argv)

	if not parse_result.success:
		return -1
	# Get initial matrix
	payoff_result = get_payoff(parse_result.m, parse_result.n)

	if not payoff_result.success:
		return -1

	m: int = payoff_result.m
	n: int = payoff_result.n

	tableau: Tableau = get_init_tableau(payoff_result.payoff, m, n)
	order = [-1] * n

	pivot_count = 0
	# while true hype...incomplete SF 10/13
	while True:
		if pivot_count == 0:
			print("Initial Tableau:")
		else:
			print("Tableau {}:".format(pivot_count))
		print(tableau)

		(tableau, pivot_row, pivot_col) = pivot_tableau(tableau)
		if pivot_count < n:
			order[pivot_count] = pivot_row

		print("Pivot: ( {}, {} )\n".format(pivot_row, pivot_col))
		pivot_count += 1

		if np.min(tableau.m[tableau.rows-1]) >= 0:
			break

	print("Final Tableau:")
	print(tableau)

	v = tableau.m[tableau.rows - 1][tableau.cols - 1]
	value = (1 / v) - tableau.k

	p1_strategy = [tableau.m[tableau.rows - 1][n + col] / v for col in range(m)]
	p2_strategy = [tableau.m[order[index]][tableau.cols - 1] / v if order[index] >= 0 else 0 for index in range(n)]

	print("\nPlayer 1 Optimal Strategy: (", ", ".join(format_frac(p) for p in p1_strategy), ")")
	print("Player 2 Optimal Strategy: (", ", ".join(format_frac(q) for q in p2_strategy), ")")
	print("Value: {}".format(format_frac(value)))

	return 0


if __name__ == '__main__':
	main()

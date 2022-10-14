# Authors: Aidan Lynch, Bryce Gernon, Jim Godin, Ryan Devoe, Sam Ford
import sys  # Command line argument handling
import numpy  # Python matrix ops
import os  # Could be useful for saving output to file if desired


class ArgResult:

	def __init__(self, args : list):
		self.success = False
		self.m = 0
		self.n = 0

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
		self. n = -1
		return

class PivotResult:

	def __init__(self, success, tableau, pivot_row, pilot_col):
		self.success = success
		self.tableau = tableau
		self.pivot_row = pivot_row
		self.pivot_col = pilot_col

	'''
	* Sets a pivot result to nothing
	*
	* result: result to be nullified
	*
	'''
	def free_pivot_result(self, result):
		self.tableau.free_tableau()
		self.success = False
		self.pivot_row = None
		self.pivot_col = None
		result = None
		return

	def pivot_tableau(self, tableau):
		return


class Tableau:

	def __init__(self, s_size, x_size):
		self.s_size = s_size
		self.x_size = x_size
		self.rows = s_size + 1
		self.cols = x_size + s_size + 1
		self.k = 0
		self.m = None  # Generate m here

	def __str__(self):
		for row in range(self.rows):
			for col in range(self.cols):
				print("%6.2f ", self.m[row][col])
				print("\n")

	def get_init_tableau(self, payoff, m, n):
		return

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
def parse_args( argc : int, argv : list) -> ArgResult:
	result = ArgResult(argv)

	# do we want to prompt for input if
	# rows and cols not provided? - SF 10/13
	if(argc != 3):
		result.m = -1
		result.n = -1
		return result
	
    # parse row and column numbers
	try:
		m : int = int(argv[1])
		n : int = int(argv[2])
	except ValueError:
		result.m = -1
		result.n = -1
		return result

	result.m = m
	result.n = n
	result.success = True
	return result

def get_payoff (m : int, n : int) -> PayoffResult:
	result = PayoffResult(m,n)
	# initialize a mxn numpy array
	result.payoff = numpy.zeros((m,n))
	result.m = m
	result.n = n

	#string interpolation
	print(f"Please enter the {m} by {n} payoff matrix below."
	"\nSeparate rows by new lines and columns by spaces: \n")
	
	mat_str : str = ""
	row_els : list = []
	r_count : int = -1
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
				num : float = float(row_els[col])
				result.payoff[lineNum][col]  = num
			except ValueError:
				print("Couldn't convert input string to floats")
				result.success = False
				free_2d_arr(result.payoff, m)
				return result
		#endfor
		lineNum +=1
	#endwhile
	result.success = True
	return result


def main():
	for arg in sys.argv:
		print(arg)

	parse_result : ArgResult = parse_args(len(sys.argv),sys.argv)
	
	if(parse_result.success == False):
		return -1

	payoff_result = get_payoff(parse_result.m, parse_result.n)
	
	if(payoff_result.success == False):
		return -1


	return 0
if __name__ == '__main__':
	main()

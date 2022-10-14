# Authors: Aidan Lynch, Bryce Gernon, Jim Godin, Ryan Devoe, Sam Ford
import sys  # Command line argument handling
import numpy  # Python matrix ops
import os  # Could be useful for saving output to file if desired

'''
 * Class for storing the result of parsing command line arguments
 *
 * success: parsing of command line arguments was successful
 * m: number of rows
 * n: number of columns
 '''
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

'''
 * Class to store a pivot result
 *
 * success: if the pivot was successful
 * tableau: tableau resulting from pivot\
 * pivot_row: row of the pivot used
 * pivot_col: col of the pivot used
 '''
class PivotResult:

	def __init__(self):
		self.success = False
		self.tableau = None
		self.pivot_row = -1
		self.pivot_col = -1

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
		return

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
		self.m = numpy.zeros((self.rows,self.cols))  # Generate m here

	# equivalent to print_tableau in Aidan's simplex.c
	def __str__(self):
		tableau_str = ""
		for row in range(self.rows):
			for col in range(self.cols):
				tableau_str += f"{self.m[row][col]} "
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

'''
 * Prompt user for payoff matrix and process its entry.
 *
 * m: number of rows
 * n: number of columns
 *
 * return: payoff result structure
 '''
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
	tableau : Tableau = Tableau(m,n)
	
	min : float = sys.maxsize 
	for row in range(0, m):
		for col in range(0, n):
			if(payoff[row][col] < min):
				min = payoff[row][col]
	
	# Python ternary assignment of booster val k
	k : float = 1 - min if (min < 1) else 0

	# populate the initial tableau so that every entry >= 
	# in the elif the == will eval to 1 or 0 since
	# True or False is equiv to those respectively
	for row in range(0, m):
		for col in range(0, n):
			if( col < n ):
				tableau.m[row][col] = payoff[row][col] + k \
				if (row < m) else -1
			elif(col < n + m): 
				tableau.m[row][col] = (float) (row == col - n) \
				if (row < m) else 0
			else:
				tableau.m[row][col] = (float) (row < m)

	return tableau

'''
 * Pivots the provided tableau
 *
 * tableau: struct to pivot
 '''
def pivot_tableau(tableau : Tableau) -> PivotResult:
	result : PivotResult = PivotResult()
	result.tableau = Tableau(tableau.s_size, tableau.x_size)
	result.tableau = tableau.k

	#rest for me later on or whoever works next.
	return result
'''
 * Runs the simplex method on the supplied payoff matrix.
 *
 * argc: number of command line arguments
 * argv: array of tokens
 *
 * return: 0 on successful execution
 '''
def main():
	for arg in sys.argv:
		print(arg)

	parse_result : ArgResult = parse_args(len(sys.argv),sys.argv)
	
	if(parse_result.success == False):
		return -1

	payoff_result = get_payoff(parse_result.m, parse_result.n)
	
	if(payoff_result.success == False):
		return -1

	m : int = payoff_result.m
	n : int = payoff_result.n
	print( m, n)
	# set order of x variables to be -1 for the m rows
	order : list = [-1] * m 
	tableau : Tableau = get_init_tableau(payoff_result.payoff, m, n)
	print("Initial Tableau:")
	print(tableau)
	
	pivot_count = 0

	# while true hype...incomplete SF 10/13
	while(True):
		pivot_result : PivotResult = pivot_tableau(tableau)
		
		#placeholder for no perma-loop
		if(True == True):
			break
		#do something maybe...
		if(pivot_result.success == True):
			break
		#get outta the loop
		else: 
			break
		
		pviot_count += 1

	return 0

if __name__ == '__main__':
	main()

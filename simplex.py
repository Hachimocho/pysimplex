# Authors: Aidan Lynch, Bryce Gernon, Jim Godin, Ryan Devoe, Sam Ford
import sys  # Command line argument handling
import numpy  # Python matrix ops
import os  # Could be useful for saving output to file if desired


class ArgResult:

	def __init__(self, args):
		self.success = False
		self.m = 0
		self.n = 0


class PayoffResult:

	def __init__(self, m, n):  # Equivalent to get_payoff
		self.success = False
		self.payoff = 0.0
		self.m = 0
		self.n = 0

	def free_payoff_result(self):
		return


class PivotResult:

	def __init__(self, success, tableau, pivot_row, pilot_col):
		self.success = success
		self.tableau = tableau
		self.pivot_row = pivot_row
		self.pivot_col = pilot_col

	def free_pivot_result(self, result):
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

	def free_tableau(self):
		return


def free_2d_arr(arr, rows):
	return


def print_usage():
	print("usage: simplex m n\n")
	print("\tm: number of rows, integer greater than 0\n")
	print("\tn: number of columns, integer greater than 0\n")


def main():
	for arg in sys.argv:
		print(arg)


if __name__ == '__main__':
	main()

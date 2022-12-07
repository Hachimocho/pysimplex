# Authors: Aidan Lynch, Bryce Gernon, Jim Godin, Ryan Devoe, Sam Ford
from ctypes import Union
import sys
from typing import Tuple  # Command line argument handling
import numpy  # Python matrix ops
from fractions import Fraction
import os  # Could be useful for saving output to file if desired
import tkinter as tk  # GUI
from functools import partial  # Helper for GUI methods

import numpy as np


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
	def __init__(self, base_rows, base_cols):
		self.rows = base_rows + 1
		self.cols = base_cols + base_rows + 1
		self.k = 0
		# print( self.rows, self.cols, "in tableau constructor")
		# numpy makes 2 for loops in C into a line of code - SF 10/13
		self.m = numpy.zeros((self.rows, self.cols)).astype('object')  # Generate m here
		for row, _ in enumerate(self.m):
			for col, _ in enumerate(self.m[row]):
				self.m[row][col] = Fraction(0)
		self.finished = False

	# equivalent to print_tableau in Aidan's simplex.c
	def __str__(self):
		tableau_str = ""
		for row in range(self.rows):
			if row == self.rows - 1:
				tableau_str += "-" * (8 * self.cols + 2) + "\n"
			for col in range(self.cols):
				if col == self.cols - 1 or col == self.rows + self.cols:
					tableau_str += "|"

				frac = Fraction(self.m[row][col])
				tableau_str += "{:^8}".format(format_frac(frac))
			if row < self.rows - 1:
				tableau_str += "\n"
		return tableau_str

	def pivot_tableau(self):
		pivot_col = np.argmin(self.m[self.rows - 1])
		min_value = sys.maxsize
		pivot_row = Fraction(-1)
		for row, entry in enumerate(np.swapaxes(self.m, 0, 1)[pivot_col][0:-1]):
			if (entry == 0):
				value = 0
			else:
				value = Fraction(self.m[row][self.cols-1] / entry)
			if 0 < value < min_value:
				min_value = value
				pivot_row = row
		if pivot_row == -1:
			self.finished = True
			return
		pivot_value = Fraction(self.m[pivot_row][pivot_col])
		print(pivot_value)
		prev_tableau = np.copy(self.m)
		for col, _ in enumerate(self.m[pivot_row]):
			self.m[pivot_row][col] = Fraction(self.m[pivot_row][col] / pivot_value)

		for row, _ in enumerate(self.m):
			for col, _ in enumerate(self.m[row]):
				if row != pivot_row:
					self.m[row][col] = Fraction(
						self.m[row][col] - Fraction(prev_tableau[row][pivot_col] * self.m[pivot_row][col]))
		return



'''
 * Print the usage statement for this program.
 '''


def print_usage():
	print("usage: simplex m n")
	print("\tm: number of rows, integer greater than 0")
	print("\tn: number of columns, integer greater than 0")


'''
 * Prompt user for payoff matrix and process its entry.
 *
 * m: number of rows
 * n: number of columns
 *
 * return: payoff result structure
 '''

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
			if payoff[row][col] < min:
				min = payoff[row][col]

	# Python ternary assignment of booster val k
	k = Fraction(1 - min) if (min < 1) else Fraction(0)

	# populate the initial tableau so that every entry >=
	# in the elif the == will eval to 1 or 0 since
	# True or False is equiv to those respectively
	for row in range(0, tableau.rows):
		for col in range(0, tableau.cols):
			if col < n:
				tableau.m[row][col] = Fraction(payoff[row][col] + k) \
					if (row < m) else Fraction(-1)
			elif col < n + m:
				tableau.m[row][col] = Fraction((row == col - n)) \
					if (row < m) else Fraction(0)
			else:
				tableau.m[row][col] = Fraction((row < m))

	return tableau


'''
 * Pivots the provided tableau
 *
 * tableau: struct to pivot
 '''


def main_tableau():
	# Parse inputs
	return
	# parse_result: ArgResult = parse_args(len(sys.argv), sys.argv)

	if not parse_result.success:
		print_usage()
		return -1

	# Get initial matrix
	return
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

		if np.min(tableau.m[tableau.rows - 1]) >= 0:
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


class GUI(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		self.matrixAnalysisButton = tk.Button(self, text="Matrix Analysis", command=self.matrixAnalysis)
		self.matrixAnalysisButton.pack(side="top")

	def matrixAnalysis(self):
		self.subwindow = tk.Toplevel(self)
		# self.row_options = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
		# self.column_options = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
		row_options = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
		column_options = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
		self.subwindow.columnconfigure(2, weight=3)
		self.subwindow.wm_title("Your one-stop shop for matrix analysis!")
		# self.label = tk.Label(self.self.subwindow, text="Your one-stop shop for matrix analysis!")
		# self.label.pack(side="top", fill="both", expand=True)
		self.text_entry = tk.Text(self.subwindow)
		self.text_entry.grid(column=2, row=2)
		self.row_var = tk.IntVar(self)
		self.column_var = tk.IntVar(self)
		row_entry = tk.OptionMenu(self.subwindow, self.row_var, *row_options)
		column_entry = tk.OptionMenu(self.subwindow, self.column_var, *column_options)
		row_entry.grid(column=1, row=0)
		column_entry.grid(column=1, row=1)
		row_label = tk.Label(self.subwindow, text="Rows:")
		row_label.grid(row=0, column=0)
		column_label = tk.Label(self.subwindow, text="Columns:")
		column_label.grid(row=1, column=0)
		button_grid = tk.Frame(self.subwindow)
		button_grid.grid(row=0, column=2)
		#graphic_button = tk.Button(button_grid, text="Solve\nGraphically", command=self.solveGraphically)
		#graphic_button.grid(row=0, column=0)
		saddle_point_button = tk.Button(button_grid, text="Search for\nSaddle Points", command=self.findSaddle)
		saddle_point_button.grid(row=0, column=1)
		simplex_button = tk.Button(button_grid, text="Solve with\nSimplex method", command=self.solveWithSimplex)
		simplex_button.grid(row=1, column=0)
		strats_button = tk.Button(button_grid, text="Find strategies\nand game value", command=self.findStrats)
		strats_button.grid(row=1, column=1)
		self.buttons_label = tk.Label(button_grid, text="Enter the numbers of rows and columns using\nthe dropdowns "
		                                                "to the left, enter the matrix\nbelow, then press one of"
		                                                " these buttons!")
		self.buttons_label.grid(column=2, row=0, columnspan=2, rowspan=2)

	def solveGraphically(self):
		self.buttons_label.config(text="Not implemented\nyet.")
		return
		print("GRAPHICS")
		print(self.text_entry.get(0.0, tk.END))
		start = self.getTableau()
		if type(start) != Tableau:
			return

	def findStrats(self):
		tableau = self.getTableau()
		for x in range(1000):
			tableau.pivot_tableau()
		v = tableau.m[tableau.rows - 1][tableau.cols - 1]
		#value = (1 / v) - tableau.k
		order = [-1] * (tableau.cols - tableau.rows)
		v = tableau.m[tableau.rows - 1][tableau.cols - 1]
		if (v!= 0):
			value = (1 / v) - tableau.k
		else:
			value = -tableau.k
		m = tableau.rows - 1
		n = tableau.cols - tableau.rows
		p1_strategy = [tableau.m[tableau.rows - 1][n + col] / v for col in range(m)]
		p2_strategy = [tableau.m[-1][index + n] / v for index in range(n)]
		new_text = "Player 1 Optimal Strategy: (" + ", ".join(format_frac(p) for p in p1_strategy) + ")"
		new_text += "\nPlayer 2 Optimal Strategy: (" + ", ".join(format_frac(q) for q in p2_strategy) + ")"
		new_text += "\nValue: {}".format(format_frac(value))
		self.buttons_label.config(text=new_text)
		#print("\n)
		#print("Player 2 Optimal Strategy: (", ", ".join(format_frac(q) for q in p2_strategy), ")")
		#print("Value: {}".format(format_frac(value)))

	def solveWithSimplex(self):
		tableau = self.getTableau()
		if type(tableau) != Tableau:
			return
		simplex_window = tk.Toplevel(self)
		simplex_window.wm_title("Simplex Solution")
		simplex_display = tk.Label(simplex_window, text=tableau.__str__())
		simplex_display.grid(row=1, column=0, columnspan=2)
		simplex_display.config(text=tableau.__str__())
		# lbutton = tk.Button(simplex_window, text="Previous\nPivot", command=lambda )
		# lbutton.grid(row=0, column=0)
		rbutton = tk.Button(simplex_window, text="Next\nPivot", command=lambda: [self.nextPivot(tableau, simplex_display)])
		rbutton.grid(row=0, column=1)

	def findSaddle(self):
		tableau = self.getTableau()
		if type(tableau) != Tableau:
			return
		saddle_point_text = "Saddle points:\n"
		for rownum in range(tableau.rows-1):
			for columnnum in range(tableau.cols-tableau.rows):
				entry = tableau.m[rownum][columnnum]
				if (entry == np.min(tableau.m[rownum][0:tableau.cols-tableau.rows])) and (entry == np.max(np.swapaxes(tableau.m, 0, 1)[columnnum][0:tableau.rows-1])):
					saddle_point_text += str(entry) + "(" + str(rownum) + "," + str(columnnum) + ")\n"
		self.buttons_label.config(text=saddle_point_text)




	def getTableau(self):
		# initialize a mxn numpy array
		m = self.row_var.get()
		n = self.column_var.get()
		text = self.text_entry.get(0.0, tk.END)
		tableau = Tableau(m, n)
		lineNum = 0
		lines = text.split('\n')
		while lineNum < m:
			mat_str = lines[lineNum]
			row_els = mat_str.split()
			r_count = len(row_els)

			if r_count != n:
				self.buttons_label.config(text=f"Expected {n} entries in a row.\nGot {r_count}. Please fix and retry!")
				return -1

			# validate the input we got was numbers
			for col in range(0, n):
				try:
					num = Fraction(row_els[col])
					tableau.m[lineNum][col] = num
				except ValueError:
					self.buttons_label.config(text="Couldn't convert input string to fraction.\nMake sure you're only"
					                               "using integers!")
					return -1
			# endfor
			lineNum += 1
		# endwhile
		min = sys.maxsize
		for row in range(0, m):
			for col in range(0, n):
				if tableau.m[row][col] < min:
					min = tableau.m[row][col]

		#  Determine constant to add to tableau so all vals are positive
		k = Fraction(1 - min) if (min < 1) else Fraction(0)
		tableau.k = k
		for row in range(0, tableau.rows):
			for col in range(0, tableau.cols):
				if col < n:
					tableau.m[row][col] = Fraction(tableau.m[row][col] + k) \
						if (row < m) else Fraction(-1)
				elif col < n + m:
					tableau.m[row][col] = Fraction((row == col - n)) \
						if (row < m) else Fraction(0)
				else:
					tableau.m[row][col] = Fraction((row < m))
		return tableau

	def nextPivot(self, tableau, text):
		tableau.pivot_tableau()
		text.config(text=tableau.__str__())
		# v = tableau.m[tableau.rows - 1][tableau.cols - 1]
		# value = (1 / v) - tableau.k
		# n = tableau.cols - tableau.rows
		# m = tableau.rows - 1
		# order = [-1] * (tableau.cols - tableau.rows)
		#
		# p1_strategy = [tableau.m[tableau.rows - 1][n + col] / v for col in range(m)]
		# p2_strategy = [tableau.m[-1][index+n] / v for index in range(n)]
		#
		# print("\nPlayer 1 Optimal Strategy: (", ", ".join(format_frac(p) for p in p1_strategy), ")")
		# print("Player 2 Optimal Strategy: (", ", ".join(format_frac(q) for q in p2_strategy), ")")
		# print("Value: {}".format(format_frac(value)))


def main():
	windowroot = tk.Tk("gametheoryapp", "Game Theory Compendium")
	window = GUI(windowroot)
	window.pack(side="top", fill="both", expand=True)
	window.mainloop()
	sys.exit()


if __name__ == '__main__':
	main()

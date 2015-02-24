# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    LayoutSpliter.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/02/24 01:04:03 by jaguillo          #+#    #+#              #
#    Updated: 2015/02/24 01:04:04 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

#
# Split vertically or horizontally the layout.
#

class Case():

	def __init__(self, left, top, right, bottom):
		(self.left, self.top, self.right, self.bottom) = (left, top, right, bottom)

	def split(self, dir):
		if dir == "vertical":
			middle = round((self.right - self.left) / 2 + self.left, 2)
			case = Case(middle, self.top, self.right, self.bottom)
			self.right = middle
		elif dir == "horizontal":
			middle = round((self.bottom - self.top) / 2 + self.top, 2)
			case = Case(self.left, middle, self.right, self.bottom)
			self.bottom = middle
		return case

	def merge(self, cases):
		for c in cases:
			if c.right == self.right and c.left == self.left and (c.top == self.bottom or c.bottom == self.top):
				self.top = min(c.top, self.top)
				self.bottom = max(c.bottom, self.bottom)
			elif c.top == self.top and c.bottom == self.bottom and (c.right == self.left or c.left == self.right):
				self.left = min(c.left, self.left)
				self.right = max(c.right, self.right)
			else:
				continue
			c.left = c.top = c.right = c.bottom = 0
			cases.remove(c)
			return

class JulooLayoutSpliterCommand(sublime_plugin.WindowCommand):

	def cases_to_layout(self, cases):
		(cols, rows, cells) = ([], [], [])
		for c in cases:
			if not c.right in cols:
				cols.append(c.right)
			if not c.left in cols:
				cols.append(c.left)
			if not c.top in rows:
				rows.append(c.top)
			if not c.bottom in rows:
				rows.append(c.bottom)
		cols.sort()
		rows.sort()
		for c in cases:
			cells.append([cols.index(c.left), rows.index(c.top), cols.index(c.right), rows.index(c.bottom)]);
		return {"cols": cols, "rows": rows, "cells": cells};

	def layout_to_cases(self, layout):
		(cases, cols, rows, cells) = ([], layout["cols"], layout["rows"], layout["cells"])
		for c in cells:
			cases.append(Case(cols[c[0]], rows[c[1]], cols[c[2]], rows[c[3]]))
		return cases

	def run(self, **args):
		cases = self.layout_to_cases(self.window.get_layout())
		curr_case = cases[self.window.active_group()]
		if args["action"] == "split" and args["direction"] in ("vertical", "horizontal"):
			cases.append(curr_case.split(args["direction"]))
		elif args["action"] == "merge":
			curr_case.merge(cases)
		elif args["action"] == "reset":
			cases = [Case(0, 0, 1, 1)]
		self.window.run_command("set_layout", self.cases_to_layout(cases))

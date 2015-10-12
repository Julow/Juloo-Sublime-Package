# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooJump.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/10/12 19:25:59 by jaguillo          #+#    #+#              #
#    Updated: 2015/10/12 20:14:50 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

#
# JulooJump
#
# Jump by 8 lines
# TODO: Jump to next declaration
#
JUMP_BY = 8

class JulooJumpCommand(sublime_plugin.TextCommand):

	def jump_pt(self, pt, by):
		row, col = self.view.rowcol(pt)
		return self.view.text_point(row + by, 0)

	def jump_by_lines(self, by, shift):
		sels = []
		for s in self.view.sel():
			pt = self.jump_pt(s.a, by)
			if not shift:
				sels.append(sublime.Region(pt, pt))
			elif by < 0:
				sels.append(sublime.Region(pt, s.end()))
			else:
				sels.append(sublime.Region(s.begin(), pt))
		self.view.sel().clear()
		for s in sels:
			self.view.sel().add(s)

	def run(self, edit, **args):
		if not "action" in args:
			return
		if args["action"] == "up":
				self.jump_by_lines(-JUMP_BY, "shift" in args)
		elif args["action"] == "down":
				self.jump_by_lines(JUMP_BY, "shift" in args)

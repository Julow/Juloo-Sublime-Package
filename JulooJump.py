# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooJump.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/10/12 19:25:59 by jaguillo          #+#    #+#              #
#    Updated: 2015/10/12 23:07:00 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

#
# JulooJump
#
# Jump by n lines
# TODO: Jump to next declaration
#
JUMP_BY = 6

class JulooJumpCommand(sublime_plugin.TextCommand):

	def jump_pt(self, pt, by):
		row, col = self.view.rowcol(pt)
		return self.view.text_point(row + by, 0)

	def jump_by_lines(self, by, shift):
		sels = []
		for s in self.view.sel():
			pt = self.jump_pt(s.b, by)
			if not shift:
				sels.append(sublime.Region(pt, pt))
			elif by < 0:
				sels.append(sublime.Region(s.a, pt))
			else:
				sels.append(sublime.Region(s.a, pt))
		self.view.sel().clear()
		for s in sels:
			self.view.sel().add(s)
		if by < 0:
			self.view.show(sels[0])
		else:
			self.view.show(sels[-1])

	def run(self, edit, **args):
		if not "action" in args:
			return
		if args["action"] == "up":
			self.jump_by_lines(-JUMP_BY, "shift" in args)
		elif args["action"] == "down":
			self.jump_by_lines(JUMP_BY, "shift" in args)

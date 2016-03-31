# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooJump.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/10/12 19:25:59 by jaguillo          #+#    #+#              #
#    Updated: 2016/01/27 13:56:06 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

#
# JulooJump
#
# Jump to next empty line
#
# Alt+up			Jump to previous empty line
# Alt+down			Jump to next empty line
# Alt+super+left	Jump to previous '{' or '('
# Alt+super+right	Jump to next '{' or '('
#
class JulooJumpCommand(sublime_plugin.TextCommand):

	def jump_to_class(self, classes, forward, shift):
		sels = []
		for s in self.view.sel():
			pt = self.view.find_by_class(s.b, forward, classes)
			if not shift:
				sels.append(sublime.Region(pt, pt))
			elif not forward:
				sels.append(sublime.Region(s.a, pt))
			else:
				sels.append(sublime.Region(s.a, pt))
		self.view.sel().clear()
		for s in sels:
			self.view.sel().add(s)
		if not forward:
			self.view.show(sels[0])
		else:
			self.view.show(sels[-1])

	def jump_to_bracket(self, forward, shift):
		sels = []
		for s in self.view.sel():
			if forward:
				tmp = self.view.find("[{(]+", s.b)
				pt = tmp.end() if tmp != None else self.view.size() - 1
			else:
				pt = 0
				for tmp in self.view.find_all("[{(]+"):
					if tmp.end() >= s.begin():
						break
					pt = tmp.end()
			if not shift:
				sels.append(sublime.Region(pt, pt))
			elif not forward:
				sels.append(sublime.Region(s.a, pt))
			else:
				sels.append(sublime.Region(s.a, pt))
		self.view.sel().clear()
		for s in sels:
			self.view.sel().add(s)
		if not forward:
			self.view.show(sels[0])
		else:
			self.view.show(sels[-1])

	def run(self, edit, **args):
		if not "action" in args:
			return
		if args["action"] == "up":
			self.jump_to_class(sublime.CLASS_EMPTY_LINE, False, "shift" in args and args["shift"])
		elif args["action"] == "down":
			self.jump_to_class(sublime.CLASS_EMPTY_LINE, True, "shift" in args and args["shift"])
		elif args["action"] == "right":
			self.jump_to_bracket(True, "shift" in args and args["shift"])
		elif args["action"] == "left":
			self.jump_to_bracket(False, "shift" in args and args["shift"])

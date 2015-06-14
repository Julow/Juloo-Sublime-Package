# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooFocus.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/06/14 20:47:40 by juloo             #+#    #+#              #
#    Updated: 2015/06/14 21:35:15 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

#
# JulooFocus
#
# Switch group
# Switch views in a group
#
class JulooFocusCommand(sublime_plugin.WindowCommand):

	def focus_group(self, offset = 1):
		group = self.window.active_group() + offset
		self.window.focus_group(group % self.window.num_groups())

	def focus_view(self, offset = 1):
		group, index = self.window.get_view_index(self.window.active_view())
		views = self.window.views_in_group(group)
		self.window.focus_view(views[(index + offset) % len(views)])

	def run(self, **args):
		if not "action" in args:
			print("lol noob")
			return
		if args["action"] == "group_next":
			self.focus_group(1)
		elif args["action"] == "group_prev":
			self.focus_group(-1)
		elif args["action"] == "view_next":
			self.focus_view(1)
		elif args["action"] == "view_prev":
			self.focus_view(-1)
		else:
			print("lol mdr: %s" % args["action"])

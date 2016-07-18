# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    focus.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/06/14 20:47:40 by juloo             #+#    #+#              #
#    Updated: 2016/07/18 15:46:26 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin, os

#
# JulooFocus
#
# Switch group
# Switch view in group
# Move view in group
# Move view to group
#

def mod(a, m):
	return (a + m) % m

ACTIONS = {
	"group_next": lambda s, _: s.focus_group(1),
	"group_prev": lambda s, _: s.focus_group(-1),
	"view_next": lambda s, _: s.focus_view(1),
	"view_prev": lambda s, _: s.focus_view(-1),
	"move_right": lambda s, _: s.move_view(1),
	"move_left": lambda s, _: s.move_view(-1),
	"move_next": lambda s, _: s.move_to_group(1),
	"move_prev": lambda s, _: s.move_to_group(-1),
}

class JulooFocusCommand(sublime_plugin.WindowCommand):

	def focus_group(self, offset = 1):
		group = mod(self.window.active_group() + offset, self.window.num_groups())
		self.window.focus_group(group)
		self.focus_message()

	def focus_view(self, offset = 1):
		group, index = self.window.get_view_index(self.window.active_view())
		views = self.window.views_in_group(group)
		self.window.focus_view(views[mod(index + offset, len(views))])
		self.focus_message()

	def focus_message(self):
		def file_name():
			fname = self.window.active_view().file_name()
			for f in self.window.project_data()["folders"]:
				f = f["path"]
				if fname.startswith(f):
					return "*%s* %s" % (os.path.basename(f), os.path.relpath(fname, f))
			return "* %s" % os.path.basename(fname)
		sublime.status_message("[%s]" % file_name())

	def move_view(self, offset = 1):
		view = self.window.active_view()
		group, index = self.window.get_view_index(view)
		index = mod(index + offset, len(self.window.views_in_group(group)))
		self.window.set_view_index(view, group, index)

	def move_to_group(self, offset = 1):
		view = self.window.active_view()
		group = mod(self.window.active_group() + offset, self.window.num_groups())
		self.window.set_view_index(view, group, 0)

	def run(self, **args):
		if "action" in args and args["action"] in ACTIONS:
			ACTIONS[args["action"]](self, args)

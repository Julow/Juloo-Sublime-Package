# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooCursor.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/08/30 16:57:29 by juloo             #+#    #+#              #
#    Updated: 2015/08/30 18:10:07 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

savedSelections = []

class JulooCursorCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		if not "action" in args:
			return
		if args["action"] == "save":
			for s in self.view.sel():
				savedSelections.append(s)
		elif args["action"] == "restore":
			self.view.sel().add_all(savedSelections)
		elif args["action"] == "clear":
			savedSelections.clear()

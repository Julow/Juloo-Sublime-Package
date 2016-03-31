# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    side_bar.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/03/31 18:40:26 by juloo             #+#    #+#              #
#    Updated: 2016/03/31 19:40:08 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

class JulooSideBar(sublime_plugin.WindowCommand):

	current_group = 0

	def run(self):
		if self.window.is_sidebar_visible():
			self.window.set_sidebar_visible(False)
			self.window.focus_group(self.current_group)
			self.collapse_folders()
		else:
			self.current_group = self.window.active_group()
			self.window.set_sidebar_visible(True)
			sublime.set_timeout(self.focus, 50)

	def focus(self):
		self.window.run_command("reveal_in_side_bar")
		self.window.run_command("focus_side_bar")

	def collapse_folders(self):
		tmp = self.window.project_data()
		self.window.set_project_data({})
		self.window.set_project_data(tmp)

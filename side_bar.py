# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    side_bar.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/03/31 18:40:26 by juloo             #+#    #+#              #
#    Updated: 2018/12/12 12:32:31 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

class JulooSideBar(sublime_plugin.WindowCommand):

	current_group = 0

	def run(self, **args):
		if "action" in args:
			if args["action"] == "toggle":
				self.toggle()
			elif args["action"] == "clear":
				self.clear()

	def toggle(self):
		if self.window.is_sidebar_visible():
			self._hide()
		else:
			self._show()

	def clear(self):
		self.window.set_project_data({})
		if self.window.is_sidebar_visible():
			self._hide()

	def _show(self):
		self.current_group = self.window.active_group()
		self.window.set_sidebar_visible(True)
		sublime.set_timeout(self._focus, 50)

	def _hide(self):
		self.window.set_sidebar_visible(False)
		self.window.focus_group(self.current_group)

	def _focus(self):
		self.window.run_command("reveal_in_side_bar")
		self.window.run_command("focus_side_bar")

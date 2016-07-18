# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scroll.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/07/18 15:46:31 by jaguillo          #+#    #+#              #
#    Updated: 2016/07/18 17:00:24 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

class JulooScrollCommand(sublime_plugin.WindowCommand):

	def run(self, **args):
		view = self.window.active_view()
		_, v_height = view.viewport_extent()
		if args.get("half_page", False):
			offset = v_height / 3
		else:
			offset = args.get("offset", 1) * view.line_height()
		if args.get("rev", False):
			offset = -offset
		x, y = view.viewport_position()
		view.set_viewport_position((x, max(y + offset, 0)))

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scroll.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/07/18 15:46:31 by jaguillo          #+#    #+#              #
#    Updated: 2016/07/18 15:53:58 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

class JulooScrollCommand(sublime_plugin.WindowCommand):

	def run(self, **args):
		view = self.window.active_view()
		_, v_height = view.viewport_extent()
		offset = v_height / 2 if args.get("half_page", False) else 1
		if args.get("rev", False):
			offset = -offset
		x, y = view.viewport_position()
		view.set_viewport_position((x, y + offset))

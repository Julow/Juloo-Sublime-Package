# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#                                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/04/07 14:19:48 by jaguillo          #+#    #+#              #
#    Updated: 2015/04/21 18:41:07 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

class JulooCheaderCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		pattern = """#ifndef %s
# define %s



#endif
"""
		name = self.view.file_name().split('/')[-1].upper()
		name = ''.join([i if (ord(i) >= ord('a') and ord(i) <= ord('z')) or (ord(i) >= ord('A') and ord(i) <= ord('Z')) else '_' for i in name])
		self.view.run_command("juloo_write", {"data": pattern % (name, name)})

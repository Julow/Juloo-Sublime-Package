# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooCpp.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/04/07 14:14:38 by jaguillo          #+#    #+#              #
#    Updated: 2015/04/07 14:46:07 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

class JulooCppCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		pattern = """
#include "%s"

%s::%s(void)
{
}

%s::~%s(void)
{
}
"""
		name = self.view.file_name().split('/')[-1]
		className = name.split('.')[0]
		name = name.replace(".cpp", ".hpp")
		self.view.run_command("juloo_write", {"point": 0, "data": pattern % (name, className, className, className, className)})
		self.view.run_command("juloo_header", {"action": "insert"})

class JulooHppCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		pattern = """
#ifndef %s
# define %s

class	%s
{
public:
	%s(void);
	~%s(void);

private:
};

#endif
"""
		name = self.view.file_name().split('/')[-1]
		className = name.split('.')[0]
		name = ''.join([i if ord(i) >= ord('A') and ord(i) <= ord('Z') else '_' for i in name.upper()])
		self.view.run_command("juloo_write", {"point": 0, "data": pattern % (name, name, className, className, className)})
		self.view.run_command("juloo_header", {"action": "insert"})

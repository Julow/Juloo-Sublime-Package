# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooCpp.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/04/07 14:14:38 by jaguillo          #+#    #+#              #
#    Updated: 2015/04/08 14:37:22 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

class JulooCppCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		pattern = """
#include "%(hpp)s"

%(class)s::%(class)s(void)
{
}

%(class)s::%(class)s(%(class)s const &src)
{
	*this = src;
}

%(class)s::~%(class)s(void)
{
}

%(class)s			&operator=(%(class)s const &rhs)
{
	*this = src;
	return (*this);
}
"""
		name = self.view.file_name().split('/')[-1]
		className = name.split('.')[0]
		name = name.replace(".cpp", ".hpp")
		self.view.run_command("juloo_write", {"point": 0, "data": pattern % {'hpp': name, 'class': className}})
		self.view.run_command("juloo_header", {"action": "insert"})

class JulooHppCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		pattern = """
#ifndef %(hdef)s
# define %(hdef)s

class	%(class)s
{
public:
	%(class)s(void);
	%(class)s(%(class)s const &src);
	~%(class)s(void);

	%(class)s			&operator=(%(class)s const &rhs);

private:
};

#endif
"""
		name = self.view.file_name().split('/')[-1]
		className = name.split('.')[0]
		name = ''.join([i if ord(i) >= ord('A') and ord(i) <= ord('Z') else '_' for i in name.upper()])
		self.view.run_command("juloo_write", {"point": 0, "data": pattern % {'hdef': name, 'class': className}})
		self.view.run_command("juloo_header", {"action": "insert"})

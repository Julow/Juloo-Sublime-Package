# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooCpp.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/04/07 14:14:38 by jaguillo          #+#    #+#              #
#    Updated: 2015/04/17 12:49:56 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

class JulooCppCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		pattern = """#include "%(hpp)s"
// #include <iostream>

%(class)s::%(class)s(void)
{
}

%(class)s::~%(class)s(void)
{
}

// %(class)s::%(class)s(%(class)s const &src)
// {
// 	*this = src;
// }

// %(class)s			&%(class)s::operator=(%(class)s const &rhs)
// {
// 	// *this = rhs;
// 	return (*this);
// }

// std::ostream		&operator<<(std::ostream &o, %(class)s const &rhs)
// {
// 	std::cout << rhs << std::endl;
// 	return (o);
// }
"""
		self.view.run_command("juloo_header", {"action": "insert"})
		name = self.view.file_name().split('/')[-1]
		className = name.split('.')[0]
		name = name.replace(".cpp", ".hpp")
		self.view.run_command("juloo_write", {
			"point": self.view.sel()[0].begin(),
			"data": pattern % {'hpp': name, 'class': className}
		})

class JulooHppCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		pattern = """#ifndef %(hdef)s
# define %(hdef)s

// # include <ostream>
// # include <string>
// # include <exception>

class	%(class)s
{
public:
	%(class)s(void);
	virtual ~%(class)s(void);

protected:

private:
	%(class)s(%(class)s const &src);
	%(class)s			&operator=(%(class)s const &rhs);
};

// std::ostream		&operator<<(std::ostream &o, %(class)s const &rhs);

#endif
"""
		self.view.run_command("juloo_header", {"action": "insert"})
		name = self.view.file_name().split('/')[-1]
		className = name.split('.')[0]
		name = ''.join([i if ord(i) >= ord('A') and ord(i) <= ord('Z') else '_' for i in name.upper()])
		self.view.run_command("juloo_write", {
			"point": self.view.sel()[0].begin(),
			"data": pattern % {'hdef': name, 'class': className}
		})

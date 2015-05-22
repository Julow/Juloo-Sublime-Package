# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooCpp.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/04/07 14:14:38 by jaguillo          #+#    #+#              #
#    Updated: 2015/05/22 14:48:05 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

c_class_template = """#include "%(hpp)s"

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
"""

class JulooCppCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		self.view.run_command("juloo_header", {"action": "insert"})
		name = self.view.file_name().split('/')[-1]
		className = name.split('.')[0]
		name = name.replace(".cpp", ".hpp")
		self.view.run_command("juloo_write", {
			"point": self.view.sel()[0].begin(),
			"data": c_class_template % {'hpp': name, 'class': className}
		})

h_class_template = """#ifndef %(hdef)s
# define %(hdef)s

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

#endif
"""

h_interface_template = """#ifndef %(hdef)s
# define %(hdef)s

class	%(class)s
{
public:
	virtual ~%(class)s(void){}

protected:

private:
};

#endif
"""

h_enum_template = """#ifndef %(hdef)s
# define %(hdef)s

enum class	%(class)s
{
};

#endif
"""

class JulooHppCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		self.view.run_command("juloo_header", {"action": "insert"})
		name = self.view.file_name().split('/')[-1]
		className = name.split('.')[0]
		hdef = ''.join([i if ord(i) >= ord('A') and ord(i) <= ord('Z') else '_' for i in name.upper()])
		template = h_class_template
		if ord(className[1]) >= ord('A') and ord(className[1]) <= ord('Z'):
			if className[0] == 'I':
				template = h_interface_template
			elif className[0] == 'E':
				template = h_enum_template
		self.view.run_command("juloo_write", {
			"point": self.view.sel()[0].begin(),
			"data": template % {'hdef': hdef, 'class': className}
		})

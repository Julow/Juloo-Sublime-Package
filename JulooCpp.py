# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooCpp.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/04/07 14:14:38 by jaguillo          #+#    #+#              #
#    Updated: 2015/12/01 12:46:29 by jaguillo         ###   ########.fr        #
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

// %(class)s::%(class)s(%(class)s &&src)
// {
// 	*this = src;
// }

// %(class)s::%(class)s(%(class)s const &src)
// {
// 	*this = src;
// }

// %(class)s			&%(class)s::operator=(%(class)s &&rhs)
// {
// 	// *this = rhs;
// 	return (*this);
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

hdef_before = """#ifndef %(hdef)s
# define %(hdef)s

"""

hdef_after = """
#endif"""

h_class_template = """class	%(class)s
{
public:
	%(class)s(void);
	virtual ~%(class)s(void);

protected:

private:
	%(class)s(%(class)s &&src) = delete;
	%(class)s(%(class)s const &src) = delete;
	%(class)s			&operator=(%(class)s &&rhs) = delete;
	%(class)s			&operator=(%(class)s const &rhs) = delete;
};
"""

h_interface_template = """class	%(class)s
{
public:
	virtual ~%(class)s(void){}

protected:

private:
};
"""

h_enum_template = """enum class	%(class)s
{
};
"""

class JulooHppCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		hdef_enabled = self.view.sel()[0].begin() <= 0
		name = (self.view.file_name() or "Class").split('/')[-1]
		data = ""
		if hdef_enabled:
			self.view.run_command("juloo_header", {"action": "insert"})
			hdef = ''.join([i if ord(i) >= ord('A') and ord(i) <= ord('Z') else '_' for i in name.upper()])
			data += hdef_before % {'hdef': hdef}
		className = name.split('.')[0]
		template = h_class_template
		if ord(className[1]) >= ord('A') and ord(className[1]) <= ord('Z'):
			if className[0] == 'I':
				template = h_interface_template
			elif className[0] == 'E':
				template = h_enum_template
		data += template % {'class': className}
		if hdef_enabled:
			data += hdef_after % {'hdef': hdef}
		self.view.run_command("juloo_write", {
			"point": self.view.sel()[0].begin(),
			"data": data
		})

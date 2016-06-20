# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    include_sorter.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/12/11 14:06:40 by jaguillo          #+#    #+#              #
#    Updated: 2016/06/20 18:35:53 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime_plugin, sublime, re

#
# ============================================================================ #
# C/C++
#

REG_C_INCLUDE = re.compile('\s*#\s*include\s*(?:<([^>]+)>|"([^"]+)").*')

def is_c_include(line):
	m = REG_C_INCLUDE.match(line)
	if m == None:
		return None
	if m.group(1) == None:
		return (m.group(0), m.group(2), False)
	return (m.group(0), m.group(1), True)

def c_include_sort(includes):
	simple_prefixed, simple, angle, angle_prefixed = {}, {}, {}, {}
	for i in includes:
		if "/" in i[1]:
			dst = angle_prefixed if i[2] else simple_prefixed
		else:
			dst = angle if i[2] else simple
		dst[i[1]] = i
	def sort(a):
		return [a[i][0] for i in sorted(a)]
	def helper(a, b):
		if len(b) == 0:
			return a
		elif len(a) == 0:
			return b
		return a + [""] + b if len(a) > 1 or len(b) > 1 else a + b
	return helper(helper(sort(simple_prefixed), sort(simple)), helper(sort(angle), sort(angle_prefixed))) + [""]

#
# ============================================================================ #
# module
#

REG_MODULE_REQUIRE = re.compile('\s*(?:(public|private)\s+|)require\s+([^\s]+).*')

def is_module_require(line):
	m = REG_MODULE_REQUIRE.match(line)
	return (m.group(0), m.group(1) == "public", m.group(2)) if m != None else None

def module_require_sort(lines):
	def sort(lines):
		return [l[0] for l in sorted(lines, key=lambda l: (not l[1], "::" not in l[2], l[2]))]
	public, private = [], []
	for l in lines:
		(public if l[1] else private).append(l)
	return sort(public) + [""] + sort(private)

#
# ============================================================================ #
#

LANGS = [
	(["C++"], [], is_c_include, c_include_sort),
	([], ["module"], is_module_require, module_require_sort)
]

def get_lang(file_name, syntax):
	for lang in LANGS:
		for s in lang[0]:
			if s in syntax:
				return (lang[2], lang[3])
		for n in lang[1]:
			if file_name.endswith(n):
				return (lang[2], lang[3])
	raise Exception("Unsupported language %s" % syntax)

def sort_includes(view, edit):
	is_include, include_sort = get_lang(view.file_name(), view.settings().get("syntax"))
	max_row, _ = view.rowcol(view.size())
	includes = None
	def helper(includes):
		if includes != None:
			lines = include_sort(includes[0])
			r = sublime.Region(view.text_point(includes[1], 0),
				view.text_point(row, 0) - 1)
			view.replace(edit, r, "\n".join(lines))
	for row in range(max_row + 1):
		line = view.substr(view.line(view.text_point(row, 0)))
		if len(line.strip()) == 0:
			continue
		inc = is_include(line)
		if inc == None:
			helper(includes)
			includes = None
		else:
			if includes == None:
				includes = ([], row)
			print ("INCLUDE %s" % line)
			includes[0].append(inc)
	helper(includes)

class JulooIncludeSorter(sublime_plugin.EventListener):

	def on_pre_save(self, view):
		if view.settings().get("juloo_sort_include", True):
			view.run_command("juloo_sort_include")


class JulooSortInclude(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		try:
			sort_includes(self.view, edit)
		except Exception as e:
			print("JulooIncludeSort: %s" % str(e))

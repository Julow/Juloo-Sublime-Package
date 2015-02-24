# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Norme.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/02/24 01:03:56 by jaguillo          #+#    #+#              #
#    Updated: 2015/02/24 01:03:57 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin, re, math

#
# Highlight norme errors
#
class JulooNorme(sublime_plugin.EventListener):

	def on_post_save_async(self, view):
		if view.settings().get("juloo_norme_check", False) and "C++/C" in view.settings().get("syntax"):
			norme_checker(view)
		else:
			clear_checks(view)

class JulooNormeChecker(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		if args["action"] == "check":
			norme_checker(self.view)
		elif args["action"] == "clear":
			clear_checks(self.view)

reg_names = re.compile('^[a-z_0-9]+$')
reg_include = re.compile('[^#]*# *include *["<].*\.[^h][">"].*')
reg_trail = re.compile('\s+$')
reg_comma = re.compile('[,;][^ ]')
reg_keyword = re.compile('^\s*(if|while|else|return|break|continue|union|enum|struct)[^ ]')
ops = '(&&|&=|\|=|\|\||\+=|-=|/=|\*=|\^=|==|\?|:)'
reg_op = re.compile(ops + '[^ ]|[^ ]' + ops)
reg_param0 = re.compile('\(\s*(\.\.\.)?\s*\)')

def strlen_tab(s):
	l = 0
	for c in s:
		if c == '\t':
			l = math.trunc((l + 4) / 4) * 4
		else:
			l += 1
	return (l)

def clear_checks(view):
	view.erase_regions("norme_errors")
	view.erase_status("norme_juloo")

def norme_checker(view):
	scope = view.scope_name(0)
	invalids = []
	if scope.find("source.c") >= 0:
		invalids += c_checker(view)
	elif scope.find("source.makefile") >= 0:
		invalids += makefile_checker(view)
	if len(invalids) > 0:
		view.add_regions("norme_errors", invalids, "source invalid.norme", "circle", sublime.DRAW_NO_OUTLINE)
		view.set_status("norme_juloo", "Norme errors: " + str(len(invalids)))
	else:
		clear_checks(view)

def makefile_checker(view):
	invalids = []
#
# $(NAME), all, clean, fclean, re
#
	regions = view.find_by_selector("meta.function.makefile entity.name.function.makefile")
	required = ["$(NAME)", "all", "clean", "fclean", "re"]
	for r in regions:
		s = view.substr(r).strip(':')
		if s in required:
			required.remove(s)
	for q in required:
		invalids.append(sublime.Region(view.size(), view.size()))
		print("Norme Error: Makefile required '" + q + "' rule")
#
# 80 chars in a line
# 42 header
# Wildcard
#
	regions = view.lines(sublime.Region(0, view.size()));
	in_comment = False
	header = True
	line_i = 0
	for r in regions:
		line = view.substr(r)
		l = strlen_tab(line)
		if l > 80:
			invalids.append(sublime.Region(r.begin() + 80 - (line.count('\t') * 3), r.end()))
			print("Norme Error: " + str(l) + " chars in a line")
		if view.scope_name(r.begin()).find("comment.line") >= 0:
			in_comment = True
		else:
			in_comment = False
		if not in_comment and header:
			if line_i < 11:
				invalids.append(sublime.Region(r.begin(), r.begin()))
				print("Norme Error: 42 header not a top of file")
			header = False
		if not header:
			i = line.find('*')
			if i >= 0:
				invalids.append(sublime.Region(r.begin() + i, r.begin() + i + 1))
				print("Norme Error: Wildcard not allowed in Makefile")
		line_i += 1
	return invalids

def c_checker(view):
	invalids = []
	h_file = False
	if view.file_name() != None and view.file_name().endswith(".h"):
		h_file = True
#
# 5 functions per file
# Invalid function name
# Function scope bad align
# Line between function
#
	regions = view.find_by_selector("meta.function.c entity.name.function.c")
	i = 0
	global_scope = -1
	for r in regions:
		s = view.substr(r)
		if not re.match(reg_names, s):
			invalids.append(r)
			print("Norme Error: Invalid function name '" + s + "'")
		i += 1
		if not h_file and i > 5:
			invalids.append(sublime.Region(r.begin(), r.begin()))
		row = view.rowcol(r.begin())[0]
		scope = sublime.Region(view.text_point(row, 0), r.begin())
		scope_len = strlen_tab(view.substr(scope).strip('*'))
		if global_scope == -1:
			global_scope = scope_len
		elif global_scope != scope_len:
			invalids.append(scope)
			print("Norme Error: Function " + s + " bad align (" + str(scope_len) + ")")
		line = view.line(view.text_point(row - 1, 0))
		if row > 1 and not h_file and len(view.substr(line)) > 0:
			invalids.append(line)
			print("Norme Error: Must have a line between functions")
	if not h_file and i > 5:
		print("Norme Error: " + str(i) + " functions")
#
# Struct name
# Struct tab
#
	regions = view.find_by_selector("meta.class-struct-block entity.name.type")
	for r in regions:
		s = view.substr(r)
		if not re.match(reg_names, s):
			invalids.append(r)
			print("Norme Error: Invalid struct name '" + s + "'")
		if view.substr(r.begin() - 1) != '\t' and view.substr(r.end()) != '\t':
			invalids.append(sublime.Region(r.begin() - 1, r.begin()))
			print("Norme Error: No tab before struct name")
#
# 25 lines per function
#
	regions = view.find_by_selector("meta.function.c meta.block.c")
	for r in regions:
		a = view.rowcol(r.begin())
		b = view.rowcol(r.end())
		if b[0] - a[0] >= 27:
			invalids.append(sublime.Region(view.text_point(a[0] + 26, a[1]),
				view.text_point(b[0], b[1] - 1)))
			print("Norme Error: " + str(b[0] - a[0] - 1) + " lines in a function")
#
# 4 function params
# Named param or void
#
	regions = view.find_by_selector("meta.function.c meta.parens.c");
	for r in regions:
		s = view.substr(r)
		if re.match(reg_param0, s):
			invalids.append(r)
			print("Norme Error: Function must have a named param or 'void'")
		else:
			params = s.split(",");
			if len(params) > 4:
				l = 0;
				i = 0;
				while i < 4:
					l += len(params[i]) + 1;
					i += 1
				invalids.append(sublime.Region(r.begin() + l, r.end() - 1))
				print("Norme Error: " + str(len(params)) + " params in a function")
#
# Multiple empty lines
# 80 chars per lines
# Bad include
# Trailing space
# Comma space
# Keyword space
# Operator space
# Comment formating
# 42 header
#
	regions = view.lines(sublime.Region(0, view.size()));
	last_empty = False
	in_comment = False
	header = True
	line_i = 0
	for r in regions:
		line = view.substr(r)
		if view.scope_name(r.begin()).find("comment.block.c") >= 0:
			in_comment = True
		else:
			in_comment = False
		if len(line) == 0:
			if last_empty:
				invalids.append(sublime.Region(r.begin(), r.end() + 1));
				print("Norme Error: multiple empty line")
			last_empty = True
		else:
			last_empty = False
			l = strlen_tab(line)
			if l > 80:
				invalids.append(sublime.Region(r.begin() + 80 - (line.count('\t') * 3), r.end()))
				print("Norme Error: " + str(l) + " chars in a line")
			if in_comment:
				if not header and not line.startswith("** ") and not line == "/*" and not line == "*/":
					invalids.append(r)
					print("Norme Error: Comment not well formated")
			else:
				if re.match(reg_include, line):
					invalids.append(r)
					print("Norme Error: Bad include")
				reg = re.search(reg_trail, line)
				if reg != None:
					invalids.append(sublime.Region(r.begin() + reg.start(), r.begin() + reg.end()))
					print("Norme Error: Trailing space")
				commas = re.finditer(reg_comma, line)
				for reg in commas:
					invalids.append(sublime.Region(r.begin() + reg.start(), r.begin() + reg.end()))
					print("Norme Error: Comma not followed by space")
				keywords = re.finditer(reg_keyword, line)
				for reg in keywords:
					invalids.append(sublime.Region(r.begin() + reg.start() + 1, r.begin() + reg.end()))
					print("Norme Error: Keyword not followed by space")
				ops = re.finditer(reg_op, line)
				for reg in ops:
					invalids.append(sublime.Region(r.begin() + reg.start(), r.begin() + reg.end()))
					print("Norme Error: Operator not followed by space")
		if not in_comment and header:
			if line_i < 11:
				invalids.append(sublime.Region(r.begin(), r.begin()))
				print("Norme Error: 42 header not a top of file")
			header = False
		line_i += 1
#
# Slash comment
#
	regions = view.find_by_selector("comment.line");
	if len(regions) > 0:
		invalids += regions
		print("Norme Error: Slash comments")
	return invalids

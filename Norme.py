import sublime, sublime_plugin, re, math

#
# Highlight norme errors
#
class JulooNorme(sublime_plugin.EventListener):

	def on_post_save_async(self, view):
		if view.settings().get("juloo_norme_check", True) and "C++/C" in view.settings().get("syntax"):
			norme_checker(view)
		else:
			view.erase_regions("norme_errors")

class JulooNormeChecker(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		norme_checker(self.view)

reg_names = re.compile('^[a-z_0-9]+$')
reg_include = re.compile('[^#]*# *include *["<].*\.[^h][">"].*')
reg_bracket = re.compile('^\t*[\{\}]$')

def strlen_tab(s):
	l = 0
	for c in s:
		if c == '\t':
			l = math.trunc((l + 4) / 4) * 4
		else:
			l += 1
	return (l)

def norme_checker(view):
	invalids = []
#
# 5 functions per file
# Invalid function name
# Function scope bad align
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
		if i > 5:
			invalids.append(sublime.Region(r.begin(), r.begin()))
		scope = sublime.Region(view.text_point(view.rowcol(r.begin())[0], 0), r.begin())
		scope_len = strlen_tab(view.substr(scope).strip('*'))
		if global_scope == -1:
			global_scope = scope_len
		elif global_scope != scope_len:
			invalids.append(scope)
			print("Norme Error: Function " + s + " bad align (" + str(scope_len) + ")")
	if i > 5:
		print("Norme Error: " + str(i) + " functions")
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
#
	regions = view.find_by_selector("meta.function.c meta.parens.c");
	for r in regions:
		params = view.substr(r).split(",");
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
# Bracket line
#
	regions = view.lines(sublime.Region(0, view.size()));
	last_empty = False
	for r in regions:
		line = view.substr(r)
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
			if re.match(reg_include, line):
				invalids.append(r)
				print("Norme Error: Bad include")
			if line.count('{') > 0 or line.count('}') > 0:
				if not re.match(reg_bracket, line):
					invalids.append(r)
					print("Norme Error: Invalid bracket line")
#
# Slash comment
#
	regions = view.find_by_selector("comment.line");
	if len(regions) > 0:
		invalids += regions
		print("Norme Error: Slash comments")
#
# End
#
	view.add_regions("norme_errors", invalids, "source invalid.norme", "circle", sublime.DRAW_NO_OUTLINE)

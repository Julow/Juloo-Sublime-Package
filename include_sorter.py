import sublime_plugin, sublime, re

# C includes
# Sorted by:
#	- quotes ([""] then [<>])
# 	- prefix (part before any [/], empty first)
#	- file name
def c_include(m):
	quote, name = (1, m[0]) if m[0] else (0, m[1])
	prefix, _, name = name.rpartition("/")
	return (quote, prefix, name)

# makemake's module files require
# Sorted by:
#	- visibility ([public] then [private])
#	- namespace (empty goes first)
#	- name
def module_require(m):
	visi = ["public", "private", None].index(m[0])
	name = m[1]
	prefix, _, name = name.rpartition("::")
	return (visi, prefix, name)

# Python imports
# Sorted by name, [from ... import ...] are last
# When there is multiple imports, the first one count
def python_import(m):
	return ("", m[0]) if m[0] else (m[1], m[2])

#
# ============================================================================ #
#

LANGS = [
	(["C++"], [], '\s*#\s*include\s*(?:<([^>]+)>|"([^"]+)").*', c_include),
	([], ["module"], '\s*(?:(public|private)\s+|)require\s+([^\s]+).*', module_require),
	(["Python"], [], '\s*(?:import\s+(.+)|from\s+([^\s]+)\s+import\s+(.+))', python_import),
	# OCaml opens, sorted by name
	(["OCaml"], [], '\s*open\s+([^\s]+).*', lambda m: m[0]),
	# Haskell imports, sorted by name
	(["Haskell"], [], '\s*import\s+([^\s]+).*', lambda m: m[0]),
	# Java imports, sorted by name
	(["Java"], [], '\s*import\s+([^\s]+).*', lambda m: m[0])
]

def get_lang(file_name, syntax):
	for lang in LANGS:
		for s in lang[0]:
			if s in syntax:
				return (lang[2], lang[3])
		for n in lang[1]:
			if file_name.endswith(n):
				return (lang[2], lang[3])
	return None

# Sort the "includes" of in a view
# [read_include], given a line, must returns the key used to sort
# 	or None if its not an include
def sort_includes(read_include, view, edit):
	max_row, _ = view.rowcol(view.size())
	def chunks():
		lines = []
		chunk_begin = None
		chunk_end = None
		for row in range(max_row + 1):
			line_region = view.line(view.text_point(row, 0))
			line = view.substr(line_region)
			key = read_include(line)
			if key is None:
				if len(lines) > 0:
					yield lines, sublime.Region(chunk_begin, chunk_end)
					lines = []
			else:
				if len(lines) == 0:
					chunk_begin = line_region.begin()
				lines.append((line, key))
				chunk_end = line_region.end()
		if len(lines) > 0:
			yield lines, sublime.Region(chunk_begin, chunk_end)
	for lines, region in chunks():
		lines = map(lambda k: k[0], sorted(lines, key=lambda k: k[1]))
		view.replace(edit, region, "\n".join(lines))

class JulooIncludeSorter(sublime_plugin.EventListener):

	def on_pre_save(self, view):
		if view.settings().get("juloo_sort_include", True):
			view.run_command("juloo_sort_include")

class JulooSortInclude(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		v = self.view
		lang = get_lang(v.file_name() or "", v.settings().get("syntax"))
		if lang is not None:
			reg, read = lang
			reg = re.compile(reg)
			def read_include(line):
				m = reg.match(line)
				return None if m is None else read(m.groups())
			sort_includes(read_include, v, edit)

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    cursor.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/08/30 16:57:29 by juloo             #+#    #+#              #
#    Updated: 2016/05/13 18:13:53 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

#
# Selection save:
#
# ctrl+k, ctrl+backspace	clear saved selections
# ctrl+k, ctrl+s			save current selections
# ctrl+k, ctrl+r			restore saved selections
#
# Multi cursor:
#
# ctrl+shift+down			Add a cursor 1 row below
# ctrl+shift+up				Add a cursor 1 row above
#

ACTIONS = {
	"save": lambda s: s.save_cursors(),
	"restore": lambda s: s.restore_cursors(),
	"clear": lambda s: s.clear_cursors(),
	"add_up": lambda s: s.add_cursor_column(False),
	"add_down": lambda s: s.add_cursor_column(True)
}

SAVED_REGIONS_KEY = "juloo_saved_cursors"
SAVED_REGIONS_SCOPE = "comment"
SAVED_REGIONS_FLAGS = sublime.DRAW_EMPTY | sublime.DRAW_NO_FILL | sublime.PERSISTENT

TAB_SIZE = 4

class JulooCursorCommand(sublime_plugin.TextCommand):

	def __init__(self, p):
		sublime_plugin.TextCommand.__init__(self, p)

	def run(self, edit, **args):
		if "action" in args and args["action"] in ACTIONS:
			ACTIONS[args["action"]](self)

	# Save current cursors
	def save_cursors(self):
		r = self.view.get_regions(SAVED_REGIONS_KEY) + list(self.view.sel())
		self.view.add_regions(SAVED_REGIONS_KEY, r, SAVED_REGIONS_SCOPE, flags=SAVED_REGIONS_FLAGS)

	# Clear saved cursors
	def clear_cursors(self):
		self.view.add_regions(SAVED_REGIONS_KEY, [])

	# Restore saved cursors
	def restore_cursors(self):
		self.view.sel().add_all(self.view.get_regions(SAVED_REGIONS_KEY))
		self.clear_cursors()

	# Add a cursor by column
	def add_cursor_column(self, down):
		def sels():
			for s in self.view.sel():
				while self.view.rowcol(s.a)[0] != self.view.rowcol(s.b)[0]:
					line = self.view.line(s.begin())
					yield sublime.Region(s.begin(), line.end())
					s = sublime.Region(line.end(), s.end())
				yield s

		def expand_tabs(s, end=-1):
			i = 0
			l = 0
			if end < 0:
				end = len(s) * 4
			while i < len(s) and l < end:
				l += 1 if s[i] != '\t' else TAB_SIZE - (l % TAB_SIZE)
				i += 1
			return i, l

		def tab_rowcol(pt):
			row, _ = self.view.rowcol(pt)
			_, line = expand_tabs(self.view.substr(sublime.Region(self.view.text_point(row, 0), pt)))
			return (row, line)
		def tab_text_point(row, col):
			pt = self.view.text_point(row, 0)
			expanded, _ = expand_tabs(self.view.substr(self.view.line(pt)), col)
			return pt + expanded

		def inc_row(r):
			row, col = tab_rowcol(r.begin())
			size = r.size()
			while True:
				row += 1 if down else -1
				lstart = tab_text_point(row, 0)
				_, llen = expand_tabs(self.view.substr(self.view.line(lstart)))
				if llen >= col:
					size = min(size, llen - col)
					break
				if lstart == 0 or lstart >= self.view.size():
					return None
			begin = tab_text_point(row, col)
			a, b = (begin, begin + size) if r.a < r.b else (begin + size, begin)
			return sublime.Region(a, b)

		s = inc_row((max if down else min)(sels()))
		if s != None:
			self.view.sel().add(s)

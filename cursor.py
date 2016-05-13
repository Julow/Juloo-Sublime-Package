# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    cursor.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/08/30 16:57:29 by juloo             #+#    #+#              #
#    Updated: 2016/05/13 18:36:57 by jaguillo         ###   ########.fr        #
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
# Cursor move:
#
# alt+up					Move to previous paragraph
# alt+down					Move to next paragraph
#

ACTIONS = {
	"save": lambda s, _: s.save_cursors(),
	"restore": lambda s, _: s.restore_cursors(),
	"clear": lambda s, _: s.clear_cursors(),
	"add_up": lambda s, _: s.add_cursor_column(False),
	"add_down": lambda s, _: s.add_cursor_column(True),
	"move_p": lambda s, args: s.move_by_paragraph(-1 if "up" in args else 1, "shift" in args),
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
			ACTIONS[args["action"]](self, args)

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

	# Move cursors by paragraph
	def move_by_paragraph(self, d, shift):
		sels = []
		def empty_line(row):
			while True:
				row += d
				pt = self.view.text_point(row, 0)
				line_str = self.view.substr(self.view.line(pt))
				if len(line_str.strip()) == 0:
					return pt + len(line_str)
				if row < 0 or pt >= self.view.size():
					return -1
		for s in self.view.sel():
			row, _ = self.view.rowcol(s.b)
			pt = empty_line(row)
			if pt < 0:
				break
			sels.append(sublime.Region(s.a if shift else pt, pt))
		self.view.sel().clear()
		self.view.sel().add_all(sels)
		self.view.show(sels[0] if d < 0 else sels[-1])

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

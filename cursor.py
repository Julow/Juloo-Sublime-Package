# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    cursor.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/08/30 16:57:29 by juloo             #+#    #+#              #
#    Updated: 2016/10/03 17:49:05 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin, itertools

#
# Selection save:
#
# alt+x						Clear saved cursors
# alt+s						Save current cursors
# alt+shift+s				Restore saved cursors
# alt{,+shift}+r			Rotate sets of saved cursors
#
# alt{,+shift}+d			Jump to the {next,previous} saved cursor
#
# ctrl+shift+{up,down}		Add a cursor 1 row {above,below}
#
# alt+{up,down}				Move to the {previous,next} paragraph
# alt+shift+{up,down}		Select the {previous,next} paragraph
#
# alt+z						Cut selections in half
# alt+shift+z				Cut selections in half + Reverse their directions
#

ACTIONS = {
	"save": lambda s, _: s.save_cursors(),
	"restore": lambda s, _: s.restore_cursors(),
	"clear": lambda s, _: s.clear_cursors(),
	"rot": lambda s, _: s.rotate_cursors(-1),
	"rrot": lambda s, _: s.rotate_cursors(1),
	"next": lambda s, _: s.next_cursor(1),
	"prev": lambda s, _: s.next_cursor(-1),
	"add_up": lambda s, _: s.add_cursor_column(False),
	"add_down": lambda s, _: s.add_cursor_column(True),
	"move_p": lambda s, args: s.move_by_paragraph(-1 if "up" in args else 1, "shift" in args),
	"cut_sel": lambda s, args: s.cut_sel("rev" in args and args["rev"]),
}

SAVED_REGIONS_KEY = "juloo_saved_cursors.%d"
SAVED_REGIONS_SCOPE = ["comment", "selection"]
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
		self._put_regions(0, self._get_regions(0) + list(self.view.sel()))

	# Clear saved cursors
	def clear_cursors(self):
		for i, c in list(enumerate(list(self._get_all_regions()) + [[]]))[1:]:
			self._put_regions(i - 1, c)

	# Restore saved cursors
	def restore_cursors(self):
		self.view.sel().add_all(self._get_regions(0))

	# Jump to the next cursor
	def next_cursor(self, d):
		sels = []
		cursors = self._get_regions(0)
		if len(cursors) == 0:
			return
		def n(d): return -1 if d < 0 else 1 if d > 0 else 0
		for s in self.view.sel():
			nexts = [c for c in cursors if n(c.begin() - s.begin()) == d]
			if len(nexts) == 0:
				sels.append(cursors[0 if d > 0 else -1])
			else:
				sels.append(min(nexts, key=lambda c: abs(c.begin() - s.begin())))
		self.view.sel().clear()
		self.view.sel().add_all(sels)
		self.view.show(sels[0] if d < 0 else sels[-1])

	# Rotate saved cursors
	def rotate_cursors(self, d):
		cursors = list(self._get_all_regions())
		for i, c in enumerate(cursors[d:] + cursors[:d]):
			self._put_regions(i, c)

	#
	def _get_all_regions(self):
		i = 0
		has_empty = False
		while True:
			tmp = self._get_regions(i)
			if len(tmp) == 0:
				if has_empty:
					break
				has_empty = True
			yield tmp
			i += 1
	def _get_regions(self, i):
		return self.view.get_regions(SAVED_REGIONS_KEY % i)
	def _put_regions(self, i, regions):
		scope = SAVED_REGIONS_SCOPE[min(i, len(SAVED_REGIONS_SCOPE) - 1)]
		self.view.add_regions(SAVED_REGIONS_KEY % i, regions, scope, flags=SAVED_REGIONS_FLAGS)

	# Move cursors by paragraph
	def move_by_paragraph(self, d, shift):
		sels = []
		def empty_line(row):
			empty = True
			while True:
				row += d
				pt = self.view.text_point(row, 0)
				if pt == 0 or pt >= self.view.size():
					return pt
				line_str = self.view.substr(self.view.line(pt))
				if len(line_str.strip()) == 0:
					if empty:
						continue
					return pt + len(line_str)
				empty = False
		for s in self.view.sel():
			row, _ = self.view.rowcol(s.b)
			pt = empty_line(row)
			if pt < 0:
				break
			sels.append(sublime.Region(s.a if shift else pt, pt))
		self.set_selections(sels)
		self.view.show(sels[0] if d < 0 else sels[-1])

	# Cut selections in half
	def cut_sel(self, rev):
		def cut(s):
			half = s.size() / (2 if s.b >= s.a else -2)
			if rev:
				return sublime.Region(s.a + half, s.a)
			return sublime.Region(s.a, s.a + half)
		self.set_selections(list(map(cut, self.view.sel())))

	def set_selections(self, sels):
		self.view.sel().clear()
		self.view.sel().add_all(sels)

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

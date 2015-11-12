# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooCursor.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/08/30 16:57:29 by juloo             #+#    #+#              #
#    Updated: 2015/11/12 12:19:23 by jaguillo         ###   ########.fr        #
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

savedSelections = []

TAB_SIZE = 4

# add cursor
def tabs_rowcol(view, pt):
	row, _ = view.rowcol(pt)
	line = view.substr(sublime.Region(view.text_point(row, 0), pt)).expandtabs(TAB_SIZE)
	return (row, len(line))

def tabs_text_point(view, row, col):
	pt = view.text_point(row, 0)
	expanded = len(view.substr(sublime.Region(pt, view.text_point(row, col))).expandtabs(TAB_SIZE))
	return view.text_point(row, col - (expanded - col))

def next_line_fit(view, row, col, by, sel_size):
	if sel_size == 0:
		line_len = len(view.substr(view.line(view.text_point(row, 0))).expandtabs(TAB_SIZE))
		return tabs_text_point(view, row, col)
	min_len = col + sel_size
	max_row, _ = view.rowcol(view.size())
	while row >= 0 and row <= max_row:
		line_len = len(view.substr(view.line(view.text_point(row, 0))).expandtabs(TAB_SIZE))
		if line_len >= min_len:
			return tabs_text_point(view, row, col)
		row += by
	return -1

def add_cursor(view, by):
	to_add = []
	for s in view.sel():
		row, col = tabs_rowcol(view, s.begin())
		pt = next_line_fit(view, row + by, col, by, s.size())
		if pt < 0:
			continue
		to_add.append(sublime.Region(pt, pt + s.size()))
	for s in to_add:
		view.sel().add(s)
# -

def action_save(view):
	for s in view.sel():
		savedSelections.append(s)

actions = {
	"save": action_save,
	"restore": lambda view: view.sel().add_all(savedSelections),
	"clear": lambda view: savedSelections.clear(),
	"add_up": lambda view: add_cursor(view, -1),
	"add_down": lambda view: add_cursor(view, 1)
}

class JulooCursorCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		if "action" in args and args["action"] in actions:
			actions[args["action"]](self.view)

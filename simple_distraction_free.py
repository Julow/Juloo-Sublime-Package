# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    simple_distraction_free.py                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/03 19:52:04 by juloo             #+#    #+#              #
#    Updated: 2016/11/03 22:00:20 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin

SETTINGS = {
	"line_numbers": False,
	"gutter": False,
	"draw_centered": True,
	"rulers": [],
	"draw_indent_guides": False
}

STATES = [
	(False, "is_menu_visible", "set_menu_visible"),
	(False, "is_sidebar_visible", "set_sidebar_visible"),
	(False, "is_minimap_visible", "set_minimap_visible"),
	(False, "is_status_bar_visible", "set_status_bar_visible"),
	(False, "get_tabs_visible", "set_tabs_visible"),
]

class DistractionFreeMode:

	def __init__(self, win):
		self._save(win)
		self._set_active(win, True)

	def restore(self, win):
		self._set_active(win, False)

	def setup_view(self, view):
		self._setup_view(view, SETTINGS)

	def _save(self, win):
		self._saved_states = [getattr(win, get_f)() for _, get_f, _ in STATES]
		s = win.active_view().settings()
		self._saved_settings = {k: s.get(k) for k in SETTINGS}

	def _set_active(self, win, active):
		self._apply_states(win, [d for d, _, _ in STATES] if active else self._saved_states)
		self._apply_settings(win, SETTINGS if active else self._saved_settings)

	def _apply_states(self, win, states):
		for i, (_, _, set_f) in enumerate(STATES):
			getattr(win, set_f)(states[i])

	def _apply_settings(self, win, settings):
		for view in win.views():
			self._setup_view(view, settings)

	def _setup_view(self, view, settings):
		s = view.settings()
		for k, v in settings.items():
			if v == None: s.erase(k)
			else: s.set(k, v)

W_SETTINGS_KEY = "juloo_distraction_free_mode"

active_mode = None

class JulooDistractionFreeListener(sublime_plugin.EventListener):

	def on_new(self, view): self._setup(view)
	def on_load(self, view): self._setup(view)

	def _setup(self, view):
		global active_mode
		if active_mode != None:
			active_mode.setup_view(view)

class JulooSimpleDistractionFree(sublime_plugin.WindowCommand):

	def run(self, **args):
		global active_mode
		if active_mode == None:
			active_mode = DistractionFreeMode(self.window)
		else:
			active_mode.restore(self.window)
			active_mode = None

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    misc.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/02/24 01:04:00 by jaguillo          #+#    #+#              #
#    Updated: 2018/08/17 06:37:19 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin, webbrowser

#
# Util command
# Write to the file
#
# {"erase": {"begin": a, "end": b}} // erase region
# {"region": {"begin": a, "end": b}, "data": "text"} // erase region and insert text
# {"point": a, "data": "text"} // insert text
# {"data": "text"} // insert text at cursors positions
#
class JulooWriteCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		if "erase" in args:
			r = sublime.Region(int(args["erase"]["begin"]), int(args["erase"]["end"]))
			self.view.erase(edit, r)
		if not "data" in args or args["data"] == None:
			return
		if "region" in args:
			self.view.replace(edit, sublime.Region(int(args["region"]["begin"]), int(args["region"]["end"])), args["data"])
		elif "point" in args:
			self.view.insert(edit, int(args["point"]), args["data"])
		else:
			for s in self.view.sel():
				self.view.replace(edit, s, args["data"])

#
# Show the font size for 3 secs when you change it using CTRL+mouse
#
class JulooFontSizeHelper(sublime_plugin.EventListener):

	def on_load(self, view):
		def changeCallback():
			size = view.settings().get("font_size")
			sublime.status_message("[ Font Size: "+ str(size) +" ]")
		view.settings().add_on_change("font_size", changeCallback)

	def on_close(self, view):
		view.settings().clear_on_change("font_size")

#
# Open borwser command
#
class JulooOpenBrowser(sublime_plugin.TextCommand):

	def run(self, edit):
		f = self.view.file_name()
		if f != None:
			webbrowser.open(f)

#
# Hide the menu bar when a window is opened
#
class JulooHideMenuBar(sublime_plugin.EventListener):

	ok = False

	def on_new(self, view):
		if not self.ok:
			win = view.window()
			if win.is_menu_visible():
				win.set_menu_visible(False)
			self.ok = True

#
# Toggle focus of the current output panel
#
class JulooFocusPanel(sublime_plugin.WindowCommand):

	# Active output panel's view or None
	def active_output_panel(self):
		prefix = "output."
		panel = self.window.active_panel()
		if panel == None or not panel.startswith(prefix):
			return None
		panel = panel[len(prefix):]
		return self.window.find_output_panel(panel)

	# Retrieve the active output panel
	# set a flag in the panel's settings to known if its focused or not
	def run(self):
		panel = self.active_output_panel()
		if panel == None:
			return
		ps = panel.settings()
		focused = ps.get("juloo_focused", False)
		ps.set("juloo_focused", not focused)
		if focused:
			# When focusing a panel, the active group is not modified
			self.window.focus_group(self.window.active_group())
		else:
			self.window.focus_view(panel)
			sels = panel.sel()
			if len(sels) == 1 and sels[0].end() == 0:
				ends = panel.size()
				sels.clear()
				sels.add(sublime.Region(ends, ends))
				panel.show(ends)

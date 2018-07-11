# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    misc.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/02/24 01:04:00 by jaguillo          #+#    #+#              #
#    Updated: 2018/07/11 06:22:56 by juloo            ###   ########.fr        #
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

	def on_new(self, view):
		win = view.window()
		if win.is_menu_visible():
			win.set_menu_visible(False)

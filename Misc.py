# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Misc.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/02/24 01:04:00 by jaguillo          #+#    #+#              #
#    Updated: 2015/04/20 00:31:53 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin, webbrowser

#
# Util command
# Write to the file
#
# {"erase": (a, b)} // erase region
# {"region": (a, b), "data": "text"} // erase region and insert text
# {"point": a, "data": "text"} // insert text
# {"data": "text"} // insert text at cursor position
#
class JulooWriteCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		if "erase" in args:
			r = sublime.Region(args["erase"][0], args["erase"][1])
			self.view.erase(edit, r)
		if not "data" in args:
			return
		if "region" in args:
			self.view.replace(edit, sublime.Region(args["region"][0], args["region"][1]), args["data"])
		elif "point" in args:
			self.view.insert(edit, args["point"], args["data"])
		else:
			self.view.insert(edit, self.view.sel()[0].begin(), args["data"])

#
# Show the current scope in the status bar
#
class JulooScopeHelper(sublime_plugin.EventListener):

	def on_selection_modified(self, view):
		if view.settings().get("juloo_show_scope", False) and len(view.sel()) == 1 and view.sel()[0].size() == 0:
			view.set_status("scope_juloo", "[ "+ view.scope_name(view.sel()[0].a) +"]")
		else:
			view.erase_status("scope_juloo");

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

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Misc.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/02/24 01:04:00 by jaguillo          #+#    #+#              #
#    Updated: 2015/04/07 14:17:39 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin, webbrowser

#
# Util command
# Write to the file
#
class JulooWriteCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		region = None
		if "region" in args:
			region = sublime.Region(args["region"][0], args["region"][1])
		if "action" in args and args["action"] == "replace":
			self.view.replace(edit, region, args["data"])
		elif "action" in args and args["action"] == "erase":
			self.view.erase(edit, region)
		else:
			self.view.insert(edit, args["point"], args["data"])

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

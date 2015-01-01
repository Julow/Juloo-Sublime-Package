import sublime, sublime_plugin, re
from time import gmtime, strftime

#
# Insert and update the 42 header
#
c_header = """/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   %-50s :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: %-42s +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: %-40s #+#    #+#             */
/*   Updated: %-39s ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
"""

reg_file = re.compile('^[^ ]+ +([^ ]+)')
reg_by = re.compile('^[^ ]+ +By: ([^ ]+) <([^>]+)>')
reg_created = re.compile('^[^ ]+ +Created: ([^ ]+ [^ ]+) by ([^ ]+)')
reg_updated = re.compile('^[^ ]+ +Updated: ([^ ]+ [^ ]+) by ([^ ]+)')

class Header42():

	lines = []
	name = ""
	by = ("", "")
	creator = ("", "")
	updater = ("", "")
	valid = True

	def __init__(self, lines):
		self.lines = lines
		name = re.search(reg_file, lines[3])
		if name != None:
			self.name = name.group(1)
		by = re.search(reg_by, lines[5])
		if by != None:
			self.by = (by.group(1), by.group(2))
		creator = re.search(reg_created, lines[7])
		if creator != None:
			self.creator = (creator.group(1), creator.group(2))
		updater = re.search(reg_updated, lines[8])
		if updater != None:
			self.updater = (updater.group(1), updater.group(2))
		if name == None or by == None or creator == None or updater == None:
			self.valid = False

	def get(self):
		by = "%s <%s>" % self.by
		creator = "%s by %s" % self.creator
		updater = "%s by %s" % self.updater
		return c_header % (self.name, by, creator, updater)

	def update(self, view):
		self.name = view.file_name().split('/')[-1]
		self.updater = (strftime("%Y/%m/%d %H:%M:%S", gmtime()), view.settings().get("header_pseudo", self.updater[1]))

class Juloo42Header(sublime_plugin.EventListener):

	def on_pre_save(self, view):
		if view.settings().get("juloo_42_header", True):
			update_header(view)

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

def update_header(view):
	region = sublime.Region(0, view.text_point(11, 0))
	substr = view.substr(region)
	if substr.startswith(c_header[:247]) and substr.endswith(c_header[590:]):
		header = Header42(substr.split('\n'))
		if header.valid:
			header.update(view)
			view.run_command("juloo_write", {"action": "replace", "region": (region.a, region.b), "data": header.get()})
			print("Header updated")
		else:
			print("Error: Bad header.")
	else:
		print("No header detected.")

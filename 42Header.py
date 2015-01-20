import sublime, sublime_plugin, re
from time import gmtime, strftime

#
# Insert and update the 42 header
#
headers = [
	(["C++", "Java", "JavaScript", "ActionScript", "CSS", "JSON"], [], """/* ************************************************************************** */
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
"""),
	(["HTML", "XML"], [], """<!-- *********************************************************************** -->
<!--                                                                         -->
<!--                                                      :::      ::::::::  -->
<!-- %-50s :+:      :+:    :+:  -->
<!--                                                  +:+ +:+         +:+    -->
<!-- By: %-42s +#+  +:+       +#+       -->
<!--                                              +#+#+#+#+#+   +#+          -->
<!-- Created: %-40s #+#    #+#            -->
<!-- Updated: %-39s ###   ########.fr      -->
<!--                                                                         -->
<!-- *********************************************************************** -->
"""),
	([], ["s", "asm"], """;; ************************************************************************** ;;
;;                                                                            ;;
;;                                                        :::      ::::::::   ;;
;;   %-50s :+:      :+:    :+:   ;;
;;                                                    +:+ +:+         +:+     ;;
;;   By: %-42s +#+  +:+       +#+        ;;
;;                                                +#+#+#+#+#+   +#+           ;;
;;   Created: %-40s #+#    #+#             ;;
;;   Updated: %-39s ###   ########.fr       ;;
;;                                                                            ;;
;; ************************************************************************** ;;
"""),
	(["Language"], [], """# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    %-50s :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: %-42s +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: %-40s #+#    #+#              #
#    Updated: %-39s ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
""")
]

reg_file = re.compile('^[^ ]+ +([^ ]+)')
reg_by = re.compile('^[^ ]+ +By: ([^ ]+) <([^>]+)>')
reg_created = re.compile('^[^ ]+ +Created: ([^ ]+ [^ ]+) by ([^ ]+)')
reg_updated = re.compile('^[^ ]+ +Updated: ([^ ]+ [^ ]+) by ([^ ]+)')

class Header42():

	pattern = None

	lines = []
	name = ""
	by = ("", "")
	creator = ("", "")
	updater = ("", "")
	valid = False

	def __init__(self, pattern):
		self.pattern = pattern

	def set(self, user):
		self.by = (user, user + "@student.42.fr")
		self.creator = (get_42_time(), user)
		self.updater = (get_42_time(), user)

	def parse(self, lines):
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
		else:
			self.valid = True

	def get(self):
		by = "%s <%s>" % self.by
		creator = "%s by %s" % self.creator
		updater = "%s by %s" % self.updater
		return self.pattern % (self.name, by, creator, updater)

	def update(self, view):
		self.name = view.file_name().split('/')[-1]
		self.updater = (get_42_time(), view.settings().get("header_pseudo", self.updater[1]))

class Juloo42Header(sublime_plugin.EventListener):

	def on_pre_save(self, view):
		if view.settings().get("juloo_42_header", True):
			update_header(view)

class JulooHeaderCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		if args["action"] == "update":
			update_header(self.view)
		else:
			header = Header42(get_header_pattern(self.view))
			user = self.view.settings().get("header_pseudo", "Unknown")
			if user == "Unknown":
				print("Please configure your name")
			header.set(user)
			header.update(self.view)
			self.view.run_command("juloo_write", {"point": 0, "data": header.get()})

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

def get_42_time():
	return strftime("%Y/%m/%d %H:%M:%S", gmtime())

def get_header_pattern(view):
	for pattern in headers:
		syntax = view.settings().get("syntax")
		for l in pattern[0]:
			if l in syntax:
				return pattern[2]
		ext = view.file_name().lower().split('.')
		for l in pattern[1]:
			if l == ext[-1]:
				return pattern[2]
	return None

def update_header(view):
	pattern = get_header_pattern(view)
	if pattern == None:
		return
	region = sublime.Region(0, view.text_point(11, 0))
	substr = view.substr(region)
	if substr.startswith(pattern[:247]) and substr.endswith(pattern[590:]):
		header = Header42(pattern)
		header.parse(substr.split('\n'))
		if header.valid:
			header.update(view)
			view.run_command("juloo_write", {"action": "replace", "region": (region.a, region.b), "data": header.get()})
			print("Header updated")
		else:
			print("Error: Bad header.")
	else:
		print("No header detected.")

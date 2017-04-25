# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    42_header.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/02/24 01:03:39 by jaguillo          #+#    #+#              #
#    Updated: 2017/04/25 15:50:29 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime_plugin, sublime
from time import localtime, strftime
from re import search, compile
from os import environ

header_config = {
	'pattern': [
	        ":::      ::::::::",
	      ":+:      :+:    :+:",
	    "+:+ +:+         +:+",
	  "+#+  +:+       +#+",
	"+#+#+#+#+#+   +#+",
	     "#+#    #+#",
	    "###   ########.fr"],
	'offsetTop': 2,
	'offsetBottom': 2,
	'offsetMax': 10,
	'values': [ # (offset, regex, initial, update)
(3, None,												"%(file)s",				None),
(5, compile('By: +([^ ]+) +< *([^>]+) *>'),				"%(user)s <%(mail)s>",	"%(1)s <%(2)s>"),
(7, compile('Created: +([^ ]+) +([^ ]+) +by +([^ ]+)'),	"%(date)s by %(user)s",	"%(1)s %(2)s by %(3)s"),
(8, None,												"%(date)s by %(user)s",	None)
	]
}

headers = [ # headers for language or file extension
	(["PHP"], ["cpp", "hpp", "tpp"], """
// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   %                                             -50s :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: %                                     -42s +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: %                                   -40s #+#    #+#             //
//   Updated: %                                  -39s ###   ########.fr       //
//                                                                            //
// ************************************************************************** //
"""[1:-1]),
	(["C++", "Java", "JavaScript", "ActionScript", "CSS", "JSON", "GLSL", "Sass"], [], """
/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   %                                             -50s :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: %                                     -42s +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: %                                   -40s #+#    #+#             */
/*   Updated: %                                  -39s ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
"""[1:-1]),
	(["Lua"], [], """
-- ************************************************************************** --
--                                                                            --
--                                                        :::      ::::::::   --
--   %                                             -50s :+:      :+:    :+:   --
--                                                    +:+ +:+         +:+     --
--   By: %                                     -42s +#+  +:+       +#+        --
--                                                +#+#+#+#+#+   +#+           --
--   Created: %                                   -40s #+#    #+#             --
--   Updated: %                                  -39s ###   ########.fr       --
--                                                                            --
-- ************************************************************************** --
"""[1:-1]),
	(["HTML", "XML"], [], """
<!-- *********************************************************************** -->
<!--                                                                         -->
<!--                                                      :::      ::::::::  -->
<!-- %                                             -50s :+:      :+:    :+:  -->
<!--                                                  +:+ +:+         +:+    -->
<!-- By: %                                     -42s +#+  +:+       +#+       -->
<!--                                              +#+#+#+#+#+   +#+          -->
<!-- Created: %                                   -40s #+#    #+#            -->
<!-- Updated: %                                  -39s ###   ########.fr      -->
<!--                                                                         -->
<!-- *********************************************************************** -->
"""[1:-1]),
	(["ASM"], ["s", "asm", "i", "inc"], """
;; ************************************************************************** ;;
;;                                                                            ;;
;;                                                        :::      ::::::::   ;;
;;   %                                             -50s :+:      :+:    :+:   ;;
;;                                                    +:+ +:+         +:+     ;;
;;   By: %                                     -42s +#+  +:+       +#+        ;;
;;                                                +#+#+#+#+#+   +#+           ;;
;;   Created: %                                   -40s #+#    #+#             ;;
;;   Updated: %                                  -39s ###   ########.fr       ;;
;;                                                                            ;;
;; ************************************************************************** ;;
"""[1:-1]),
	(["OCaml"], ["ml", "mli"], """
(* ************************************************************************** *)
(*                                                                            *)
(*                                                        :::      ::::::::   *)
(*   %                                             -50s :+:      :+:    :+:   *)
(*                                                    +:+ +:+         +:+     *)
(*   By: %                                     -42s +#+  +:+       +#+        *)
(*                                                +#+#+#+#+#+   +#+           *)
(*   Created: %                                   -40s #+#    #+#             *)
(*   Updated: %                                  -39s ###   ########.fr       *)
(*                                                                            *)
(* ************************************************************************** *)
"""[1:-1]),
	([""], [], """
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    %                                             -50s :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: %                                     -42s +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: %                                   -40s #+#    #+#              #
#    Updated: %                                  -39s ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
"""[1:-1])
]

class Header():

	view = None
	pattern = None
	offset = 0
	values = {}

	formats = []

	def __init__(self, view):
		self.view = view
		self.values = {}
		self.formats = []
		if view.name() == None:
			self.values['file'] = "untitled"
		else:
			if view.file_name() == None:
				self.values['file'] = view.name()
			else:
				self.values['file'] = view.file_name().split('/')[-1]
		self.values['user'] = view.settings().get("pseudo", environ['USER'])
		self.values['mail'] = view.settings().get("mail", environ['MAIL'] if "MAIL" in environ else self.values['user'] + "@student.42.fr")
		self.values['date'] = strftime("%Y/%m/%d %H:%M:%S", localtime())

	def update(self, insert=False):
		for value in header_config['values']:
			l = self.view.substr(self.view.line(self.view.text_point(self.offset + value[0], 0)))
			if value[1] == None or insert:
				res = None
			else:
				res = search(value[1], l)
			if res == None:
				self.formats.append(value[2] % self.values)
			else:
				i = 1
				for g in res.groups():
					self.values[str(i)] = g;
					i += 1
				self.formats.append(value[3] % self.values)

	def insert(self):
		if len(self.view.sel()) <= 0:
			r = sublime.Region(0, 0)
		else:
			r = self.view.sel()[0]
		self.view.run_command("juloo_write", {
			"erase": {"begin": r.begin(), "end": r.end()},
			"point": r.begin(),
			"data": self.pattern[2] % tuple(self.formats) + "\n\n"
		})

	def overwrite(self):
		start = self.view.line(self.view.text_point(self.offset, 0))
		height = header_config['offsetTop'] + header_config['offsetBottom'] + len(header_config['pattern']) - 1
		end = self.view.line(self.view.text_point(self.offset + height, 0))
		self.view.run_command("juloo_write", {
			"region": {"begin": start.begin(), "end": end.end()},
			"data": self.pattern[2] % tuple(self.formats)
		})

	def search(self):
		i = 0
		while i < header_config['offsetMax']:
			j = 0
			while j < len(header_config['pattern']):
				linept = self.view.text_point(i + j, 0)
				l = self.view.substr(self.view.line(linept))
				if not header_config['pattern'][j] in l:
					break
				j += 1
			if j == len(header_config['pattern']):
				self.offset = i - header_config['offsetTop']
				return True
			i += 1
		print("Header not found")
		return False

	def load_pattern(self):
		syntax = self.view.settings().get("syntax")
		file_ext = self.view.file_name().lower().split('.')[-1] if self.view.file_name() != None else ""
		for pattern in headers:
			for l in pattern[0]:
				if l in syntax:
					self.pattern = pattern
					return True
			for l in pattern[1]:
				if l == file_ext:
					self.pattern = pattern
					return True
		if "" in syntax:
			print("lol")
		print("No header available for language " + syntax)
		return False


def update_header(view):
	header = Header(view)
	if header.load_pattern():
		if header.search():
			header.update()
			header.overwrite()

def insert_header(view):
	header = Header(view)
	if header.load_pattern():
		header.update(True)
		header.insert()


class Juloo42Header(sublime_plugin.EventListener):

	def on_pre_save(self, view):
		if view.settings().get("juloo_42_header", True):
			update_header(view)


class JulooHeaderCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		if args["action"] == "update":
			update_header(self.view)
		else:
			insert_header(self.view)

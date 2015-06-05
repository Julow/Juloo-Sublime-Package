# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    JulooInsert.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/05/21 23:31:22 by juloo             #+#    #+#              #
#    Updated: 2015/06/05 22:13:14 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime_plugin, sublime
from subprocess import Popen, PIPE, STDOUT
from os import path
try:
    from shlex import quote
except ImportError:
    from pipes import quote

shell_query = """cd %(path)s
export FILE=%(file_name)s
export LINE=%(line)d
export COLUMN=%(column)d
export TEXT=%(text)s
%(cmd)s
"""

default_cmd = "echo \"$TEXT\" | "

class JulooInsertCommand(sublime_plugin.TextCommand):

	def _insert_shell(self, cmd):
		for s in self.view.sel():
			process = Popen(["bash"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
			if s.size() == 0:
				text_region = self.view.line(s)
			else:
				text_region = s
			file_name = self.view.file_name()
			if file_name == None:
				file_name = ""
			process.stdin.write(bytes(shell_query % {
				"path": path.abspath(path.dirname(file_name)),
				"file_name": quote(path.basename(file_name)),
				"line": self.view.rowcol(s.begin())[0] + 1,
				"column": self.view.rowcol(s.begin())[1] + 1,
				"text": quote(self.view.substr(text_region)),
				"cmd": cmd
			}, 'UTF-8'))
			self.view.run_command("juloo_write", {
				"region": {"begin": s.begin(), "end": s.end()},
				"data": process.communicate()[0].decode('UTF-8').strip('\n')
			})

	def run(self, edit, **args):
		if args["what"] == "line_num":
			for s in self.view.sel():
				self.view.run_command("juloo_write", {
					"region": {"begin": s.begin(), "end": s.end()},
					"data": "%d" % self.view.rowcol(s.begin())[0] + 1
				})
		elif args["what"] == "column":
			for s in self.view.sel():
				self.view.run_command("juloo_write", {
					"region": {"begin": s.begin(), "end": s.end()},
					"data": "%d" % self.view.rowcol(s.begin())[1] + 1
				})
		elif args["what"] == "shell":
			self.view.window().show_input_panel("Shell command", default_cmd, self._insert_shell, None, None)

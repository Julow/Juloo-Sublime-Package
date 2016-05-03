# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run_command.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/05/03 22:23:49 by juloo             #+#    #+#              #
#    Updated: 2016/05/04 00:12:02 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin, os, time, subprocess, re

#
# Run a command
# (from the first opened folder)
# Save the last used command
#

class JulooRunCommandCommand(sublime_plugin.WindowCommand):

	output_panel = None
	prev_process = None

	def get_last_cmd(self):
		settings = sublime.load_settings("juloo_settings")
		return settings.get("last_run_command", "")

	def set_last_cmd(self, cmd):
		settings = sublime.load_settings("juloo_settings")
		settings.set("last_run_command", cmd)
		sublime.save_settings("juloo_settings")

	def output_line(self, s):
		self.output_panel.run_command("append", {"characters": s + "\n", "scroll_to_end": True})

	def wait_cmd(self, proc, start_time):
		for line in proc.stdout:
			self.output_line(re.sub('\033\[\d+m', "", str(line, 'UTF-8')[:-1]))
		exit_code = proc.wait()
		self.prev_process = None
		self.output_line("[end, time: %.3fs%s]" % (time.time() - start_time,
				", exit code: %d" % exit_code if exit_code != 0 else ""))

	def run_cmd(self, cmd):
		self.output_panel = self.window.create_output_panel("juloo_run_command", True)
		settings = self.output_panel.settings()
		settings.set("gutter", True)
		settings.set("color_scheme", self.window.active_view().settings().get("color_scheme"))
		self.window.run_command("show_panel", {"panel": "output.juloo_run_command"})

		if self.prev_process != None:
			self.prev_process.kill()

		os.chdir(self.window.folders()[0] or os.path.dirname(self.window.active_view().file_name()))
		self.output_line("[pwd: %s]" % os.getcwd())
		self.output_line("[cmd: %s]" % cmd)

		start_time = time.time()
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		self.prev_process = proc
		sublime.set_timeout_async(lambda: self.wait_cmd(proc, start_time), 0)

	def run(self, **args):
		def on_done(cmd):
			self.set_last_cmd(cmd)
			self.run_cmd(cmd)
		self.window.show_input_panel("Command", self.get_last_cmd(), on_done, None, None)

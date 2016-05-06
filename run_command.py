# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run_command.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/05/03 22:23:49 by juloo             #+#    #+#              #
#    Updated: 2016/05/06 17:53:43 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin, os, time, subprocess, re, signal, threading

#
# Run a command
# (from the first opened folder)
# Save the last used command
#

running_process = []

class JulooKillCommandCommand(sublime_plugin.WindowCommand):

	def run(self, **args):
		global running_process
		for p in running_process:
			if p != None and p.returncode == None:
				os.close(p.stdout.fileno())
				os.killpg(os.getpgid(p.pid), signal.SIGKILL)
				p.wait()
		running_process = []

MAX_OUTPUT_LINE = 1000

class JulooRunCommandCommand(sublime_plugin.WindowCommand):

	output_panel = None
	output_proc = None

	def get_last_cmd(self):
		settings = sublime.load_settings("juloo_settings")
		return settings.get("last_run_command", "")

	def set_last_cmd(self, cmd):
		settings = sublime.load_settings("juloo_settings")
		settings.set("last_run_command", cmd)
		sublime.save_settings("juloo_settings")

	def output_line(self, s):
		self.output_panel.run_command("append", {"characters": s + "\n", "scroll_to_end": True})

	def run_cmd(self, cmd):
		global running_process
		self.output_panel = self.window.create_output_panel("juloo_run_command", True)
		settings = self.output_panel.settings()
		settings.set("gutter", True)
		settings.set("color_scheme", self.window.active_view().settings().get("color_scheme"))
		self.window.run_command("show_panel", {"panel": "output.juloo_run_command"})

		os.chdir(self.window.folders()[0] or os.path.dirname(self.window.active_view().file_name()))

		self.output_line("[pwd: %s]" % os.getcwd())
		self.output_line("[cmd: %s]" % cmd)

		start_time = time.time()
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
				shell=True, preexec_fn=os.setsid)
		running_process.append(proc)

		def wait_cmd():
			global running_process
			line_count = 0
			for line in proc.stdout:
				if line_count < MAX_OUTPUT_LINE and self.output_proc.pid == proc.pid:
					self.output_line(re.sub('\033\[\d+m', "", str(line, 'UTF-8')[:-1]))
					line_count += 1
				elif line_count == MAX_OUTPUT_LINE:
					self.output_line("[output too big]")
					line_count += 1
			exit_code = proc.wait()
			self.output_line("[end, time: %.3fs%s%s]" % (time.time() - start_time,
					", exit code: %d" % exit_code if exit_code != 0 else "",
					", cmd: %s" % cmd if self.output_proc.pid != proc.pid else ""))
			running_process = [p for p in running_process if p.returncode == None]

		self.output_proc = proc
		thread = threading.Thread(target=wait_cmd)
		thread.deamon = True
		thread.start()

	def run(self, **args):
		def on_done(cmd):
			self.set_last_cmd(cmd)
			self.run_cmd(cmd)
		self.window.show_input_panel("Command", self.get_last_cmd(), on_done, None, None)

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    side_bar.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/03/31 18:40:26 by juloo             #+#    #+#              #
#    Updated: 2016/08/31 20:24:01 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime, sublime_plugin, os

def read_gitignore(gitignore):
	rules = []
	try:
		with open(gitignore) as f:
			for line in f:
				line = line.strip()
				if line.startswith("#"):
					continue
				rules.append(line)
	except Exception:
		pass
	return rules

class JulooSideBar(sublime_plugin.WindowCommand):

	current_group = 0

	updated_gitignore = set()

	def run(self, **args):
		if "action" in args:
			if args["action"] == "toggle":
				self.toggle()
			elif args["action"] == "clear":
				self.clear()

	def toggle(self):
		(self._hide if self.window.is_sidebar_visible() else self._show)()

	def clear(self):
		self.window.set_project_data({})
		self.updated_gitignore.clear()
		if self.window.is_sidebar_visible():
			self._hide()

	def _show(self):
		self._check_gitignores()
		self.current_group = self.window.active_group()
		self.window.set_sidebar_visible(True)
		sublime.set_timeout(self._focus, 50)

	def _hide(self):
		self.window.set_sidebar_visible(False)
		self.window.focus_group(self.current_group)
		self._collapse_folders()

	def _focus(self):
		self.window.run_command("reveal_in_side_bar")
		self.window.run_command("focus_side_bar")

	def _collapse_folders(self):
		# tmp = self.window.project_data()
		# self.window.set_project_data({})
		# self.window.set_project_data(tmp)
		pass

	def _check_gitignores(self):
		project_data = self.window.project_data()
		updated = False
		for folder in project_data["folders"]:
			if folder["path"] not in self.updated_gitignore:
				self.updated_gitignore.add(folder["path"])
				file_exclude_patterns = set(folder.get("file_exclude_patterns", []))
				folder_exclude_patterns = set(folder.get("folder_exclude_patterns", []))
				for r in read_gitignore(os.path.join(folder["path"], ".gitignore")):
					if r.endswith("/"):
						folder_exclude_patterns.add(r[:-1])
					elif r.endswith("/*"):
						folder_exclude_patterns.add(r[:-2])
					else:
						file_exclude_patterns.add(r)
				folder["file_exclude_patterns"] = list(file_exclude_patterns)
				folder["folder_exclude_patterns"] = list(folder_exclude_patterns)
				updated = True
		if updated:
			self.window.set_project_data(project_data)

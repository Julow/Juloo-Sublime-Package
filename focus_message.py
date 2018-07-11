import sublime, sublime_plugin, os

# Show the focused view's name in the status bar
# Prefixes:
# 	!	read only
# 	?	no file on disk
# 	*	unsaved changes

class JulooFocusMessage(sublime_plugin.EventListener):

	def on_activated(self, view):
		sublime.status_message("".join([
			"[ ",
			"!" if view.is_read_only() else "",
			"?" if view.file_name() is None else "",
			"*" if view.is_dirty() else "",
			os.path.basename(view.name() or view.file_name() or "untitled"),
			" ]"
		]))

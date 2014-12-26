import sublime, sublime_plugin

#
# Highlight norme errors
#
class JulooNorme(sublime_plugin.EventListener):

	def on_post_save_async(self, view):
		functions = view.find_by_selector("meta.function.c meta.block.c")
		invalids = []
		if len(functions) > 5:
			i = 5
			while i < len(functions):
				invalids.append(functions[i])
				i += 1
			print("Norme Error: " + str(len(functions)) + " functions")
		for f in functions:
			a = view.rowcol(f.begin())
			b = view.rowcol(f.end())
			if b[0] - a[0] >= 27:
				invalids.append(sublime.Region(view.text_point(a[0] + 26, a[1]),
					view.text_point(b[0] - 1, b[1])))
				print("Norme Error: " + str(b[0] - a[0] - 1) + " lines in a function")
		view.add_regions("norme_errors", invalids, "invalid.norme", "circle", sublime.DRAW_NO_OUTLINE)

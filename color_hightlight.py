# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ColorHightlight.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/02/24 01:04:07 by jaguillo          #+#    #+#              #
#    Updated: 2015/08/30 18:18:28 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os, re, sublime, sublime_plugin, colorsys

#
# Highlight colors in code
#

#	RGBA	rgba(RRR, GGG, BBB, A.A)
# rgb(50, 150, 200)
# rgba(50, 150, 200, 0.5)
#	ARGB	argb(AAA, RRR, GGG, BBB)
# argb(255, 50, 150, 200)
#	HEX		#RRGGBBAA
# #A98
# #A98F
# #AA9988
# #AA9988FF
#	INT		0xAARRGGBB
# 0x5599FF
# 0xFFAA443F
#	HSLA	hsla(HHH, SSS, LLL, A.A)
# hsl(100, 50, 50)
# hsla(100, 50%, 50%, 0.5)
#	Float Array	[ R, G, B, A ]
# [0.55555, 0.1, 0.8, 0.5]
# {0.55555F, 0.1F, 0.8F, 1F}
#

cache_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "colorHighlightCache/")

float_r = '\s*(0(?:\.[0-9]+)?|1(?:\.0+)?)[fF]?\s*'

rgb_regex = re.compile('a?rgba?\( *(\d{1,3}) *, *(\d{1,3}) *, *(\d{1,3}) *(?:, *(\d{0,3}(?:\.\d+)?) *)?\)')
hsl_regex = re.compile('hsla?\( *(\d{1,3}) *, *(\d{1,3})%? *, *(\d{1,3})%? *(?:, *(\d?(?:\.\d+)?) *)?\)')
float_regex = re.compile('(?:\{|\[)'+ float_r +','+ float_r +','+ float_r +'(?:,'+ float_r +')?(?:\}|\])')

class Color():

	r = 0
	g = 0
	b = 0
	a = 255
	valid = True

	def __init__(self, color):
		if color.find("rgb") == 0:
			s = re.search(rgb_regex, color)
			(r, g, b, a) = s.groups()
			self.r = int('0'+ r)
			self.g = int('0'+ g)
			self.b = int('0'+ b)
			if a == None:
				self.a = 255
			else:
				self.a = int(float('0'+ a) * 255)
		elif color.find("argb") == 0:
			s = re.search(rgb_regex, color)
			(a, r, g, b) = s.groups()
			if b == None:
				self.valid = False
			else:
				self.r = int('0'+ r)
				self.g = int('0'+ g)
				self.b = int('0'+ b)
				self.a = int('0'+ a)
		elif color.find("hsl") == 0:
			s = re.search(hsl_regex, color)
			(h, s, l, a) = s.groups()
			rgb = colorsys.hls_to_rgb(float('0'+ h) / 360, float('0'+ s) / 100, float('0'+ l) / 100)
			self.r = int(rgb[0] * 255)
			self.g = int(rgb[1] * 255)
			self.b = int(rgb[2] * 255)
			if a == None:
				self.a = 255
			else:
				self.a = int(float('0'+ a) * 255)
		elif color.find("0x") == 0:
			length = len(color) - 2
			if length == 6:
				(a, r, g, b) = ("FF", color[2:4], color[4:6], color[6:8])
			elif length == 8:
				(a, r, g, b) = (color[2:4], color[4:6], color[6:8], color[8:])
			else:
				self.valid = False
				return
			self.r = self._htoi(r)
			self.g = self._htoi(g)
			self.b = self._htoi(b)
			self.a = self._htoi(a)
		elif color.find("#") == 0:
			length = len(color) - 1
			if length == 3 or length == 4:
				if length == 3:
					(r, g, b, a) = (color[1:2], color[2:3], color[3:4], "F")
				else:
					(r, g, b, a) = (color[1:2], color[2:3], color[3:4], color[4])
				r += r
				g += g
				b += b
				a += a
			elif length == 6:
				(r, g, b, a) = (color[1:3], color[3:5], color[5:7], "FF")
			elif length == 8:
				(r, g, b, a) = (color[1:3], color[3:5], color[5:7], color[7:])
			else:
				self.valid = False
				return
			self.r = self._htoi(r)
			self.g = self._htoi(g)
			self.b = self._htoi(b)
			self.a = self._htoi(a)
		elif color.find("{") == 0 or color.find("[") == 0:
			s = re.search(float_regex, color)
			(r, g, b, a) = s.groups()
			self.r = int(float(r) * 255)
			self.g = int(float(g) * 255)
			self.b = int(float(b) * 255)
			if a == None:
				self.a = 255
			else:
				self.a = int(float(a) * 255)

	def _htoi(self, hex):
		return int(hex, 16)

	def _itoh(self, n):
		return (('0'+ hex(n)[2:])[-2:]).upper()

	def to_hsl(self):
		c = colorsys.rgb_to_hls(self.r / 255, self.g / 255, self.b / 255)
		hsl = str(round(c[0] * 360)) +", "+ str(round(c[1] * 100)) +"%, "+ str(round(c[2] * 100)) +"%"
		if self.a == 255:
			return "hsl("+ hsl +")"
		else:
			return "hsla("+ hsl +", "+ str(round(self.a / 255, 2)) +")"

	def to_int(self):
		i = "0x"
		if self.a != 0:
			i += self._itoh(self.a)
		return i + self._itoh(self.r) + self._itoh(self.g) + self._itoh(self.b)

	def to_hex(self):
		h = "#"+ self._itoh(self.r) + self._itoh(self.g) + self._itoh(self.b)
		if self.a != 255:
			h += self._itoh(self.a)
		return h

	def to_rgb(self):
		rgb = str(self.r) +", "+ str(self.g) +", "+ str(self.b)
		if self.a == 255:
			return "rgb("+ rgb +")"
		else:
			if self.a == 0:
				a = "0"
			else:
				a = str(round(self.a / 255, 2))
			return "rgba("+ rgb +", "+ a +")"

	def sublime_hex(self):
		h = "#"+ self._itoh(self.r) + self._itoh(self.g) + self._itoh(self.b)
		if self.a == 0:
			h += "01"
		else:
			h += self._itoh(self.a)
		return h

	def contrasted_hex(self):
		# if self.r < 10 and self.g < 10 and self.b < 10:
		# 	return "#FFFFFFFF"
		# else:
		return "#000000FF"

lastColorRegions = None
resourceCache = None

class JulooColorConvert(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		global lastColorRegions
		if lastColorRegions != None:
			arg = args["to"]
			i = len(lastColorRegions) - 1
			while i >= 0:
				r = lastColorRegions[i]
				if arg == "hex":
					self.view.replace(edit, r[0], r[1].to_hex())
				elif arg == "rgb":
					self.view.replace(edit, r[0], r[1].to_rgb())
				elif arg == "hsl":
					self.view.replace(edit, r[0], r[1].to_hsl())
				else:
					self.view.replace(edit, r[0], r[1].to_int())
				i -= 1

class JulooColorHighlight(sublime_plugin.EventListener):

	color_regex = '(#|0x)[0-9a-fA-F]{8}|(#|0x)[0-9a-fA-F]{6}|#[0-9a-fA-F]{3,4}|(?:a?rgba?\( *\d{1,3} *, *\d{1,3} *, *\d{1,3} *(?:, *\d{0,3}(?:\.\d+)? *)?\))|(?:hsla?\( *\d{1,3} *, *\d{1,3}%? *, *\d{1,3}%? *(?:, *\d{0,3}(?:\.\d+)? *)?\))|(?:\{|\\[)'+ float_r +','+ float_r +','+ float_r +'(?:,'+ float_r +')?(?:\}|\\])'
	xml_template = """	<dict>
			<key>scope</key>
			<string>juloo.color.{2}</string>
			<key>settings</key>
			<dict>
				<key>background</key>
				<string>{0}</string>
				<key>foreground</key>
				<string>{0}</string>
			</dict>
		</dict>
		<dict>
			<key>scope</key>
			<string>juloo.colortext.{2}</string>
			<key>settings</key>
			<dict>
				<key>fontStyle</key>
				<string>normal</string>
				<key>background</key>
				<string>{0}</string>
				<key>foreground</key>
				<string>{1}</string>
			</dict>
		</dict>
	"""

	def get_xml_path(self, id):
		return cache_path + str(id) +".tmTheme"

	def get_full_path(self, theme_path):
		return os.path.join(sublime.packages_path(), os.path.normpath(theme_path))

	def get_colored_regions(self, view):
		regions = []
		for sel in view.sel():
			if sel.size == 0:
				continue
			elif len(regions) > 15:
				break;
			line = view.line(sel)
			startPos = max(line.begin(), sel.begin() - 27)
			endPos = min(sel.end() + 27, line.end())
			m = sublime.Region(startPos, startPos)
			max_iteration = 4
			while max_iteration > 0:
				m = view.find(self.color_regex, m.end())
				if m == None or m.end() > endPos:
					break
				if m.contains(sel):
					regions.append((m, Color(view.substr(m))))
					break
				max_iteration -= 1
		return regions

	def on_close(self, view):
		if view.settings().has("old_color_scheme"):
			old_color_scheme = view.settings().get("old_color_scheme")
			view.settings().set("color_scheme", old_color_scheme)
			view.settings().erase("old_color_scheme")
		full_path = self.get_full_path(self.get_xml_path(view.id()))
		if os.path.exists(full_path):
			os.remove(full_path)

	def get_res(self, name):
		global resourceCache
		if resourceCache == None:
			resourceCache = (name, sublime.load_resource(name))
		if resourceCache[0] != name:
			resourceCache = None
			return self.get_res(name)
		return resourceCache[1]

	def on_selection_modified_async(self, view):
		if not view.settings().get("juloo_color_enabled", False):
			return
		global lastColorRegions
		regions = self.get_colored_regions(view)
		if lastColorRegions != None and len(regions) != len(lastColorRegions):
			i = 0;
			while i < len(lastColorRegions):
				view.erase_regions("colorhightlight-" + str(i))
				view.erase_regions("texthightlight-" + str(i))
				i += 1
		if len(regions) == 0:
			view.erase_status("color_juloo")
			if view.settings().has("old_color_scheme"):
				view.settings().erase("old_color_scheme")
				view.settings().erase("color_scheme")
				full_path = self.get_full_path(self.get_xml_path(view.id()))
				if os.path.exists(full_path):
					os.remove(full_path)
		else:
			lastColorRegions = regions
			if len(regions) == 1:
				view.set_status("color_juloo", "[ Color: "+ regions[0][1].to_hex() +", "+ regions[0][1].to_rgb() +", "+ regions[0][1].to_int() +", "+ regions[0][1].to_hsl() +" ]")
			elif len(regions) > 1:
				status = "[ Colors: "
				for r in regions:
					status += r[1].to_hex()
					status += ", "
				view.set_status("color_juloo", status + "]")
			else:
				view.erase_status("color_juloo")
			if view.settings().has("old_color_scheme"):
				color_scheme = view.settings().get("old_color_scheme")
			else:
				color_scheme = view.settings().get("color_scheme")
				view.settings().set("old_color_scheme", color_scheme)
			data = self.get_res(color_scheme)
			index = data.find("</array>")
			xml = ""
			i = 0
			for r in regions:
				s = str(i)
				view.add_regions("colorhightlight-" + s, [r[0]], "juloo.color." + s, "circle", sublime.HIDDEN)
				view.add_regions("texthightlight-" + s, [r[0]], "juloo.colortext." + s, "", sublime.DRAW_NO_OUTLINE)
				xml += self.xml_template.format(r[1].sublime_hex(), r[1].contrasted_hex(), s)
				i += 1
			data = data[:index] + xml + data[index:]
			if not os.path.exists(self.get_full_path(cache_path)):
				os.mkdir(self.get_full_path(cache_path))
			f = open(self.get_full_path(self.get_xml_path(view.id())), "wb")
			f.write(data.encode("utf-8"))
			f.close()
			view.settings().set("color_scheme", self.get_xml_path(view.id()).replace(sublime.packages_path(), "Packages"))

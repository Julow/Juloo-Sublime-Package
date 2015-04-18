# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/04/18 23:01:26 by juloo             #+#    #+#              #
#    Updated: 2015/04/19 01:24:46 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sublime_plugin, sublime
from re import compile, search

reg_member = compile('(virtual\s+)?(\w+)\s+(const\s+)?([&*])?([^~\s\(]+)\(\s*([^\)]+)\s*\)\s*(const\s*)?(?:throw\s*\(\s*([^\s\)]+)\s*\)\s*)?;');
reg_property = compile('(\w+)\s+(const\s+)?([&*])?(\w+)\s*;');
reg_visibility = compile('(public|private|protected):')
reg_param = compile('[\w]+\s+(const\s+)?([&*]?)(\w+)')

class Class():

	name = None

	methods = []
	properties = []

	view = None

	def __init__(self, name, view):
		self.name = name
		self.view = view

	def parse(self, region):
		lines = self.view.lines(region)
		visibility = "private"
		for l in lines:
			line = self.view.substr(l)
			m = reg_visibility.search(line)
			if m != None:
				visibility = m.group(1)
				continue
			m = reg_member.search(line)
			if m != None:
				self.methods.append(Method(self, m, visibility))
				continue
			m = reg_property.search(line)
			if m != None:
				self.properties.append(Property(m, visibility))

	def toCpp(self):
		s = ""
		for m in self.methods:
			s += m.toCpp()
			s += "\n\n"
		return s

class Property():

	visibility = "private"
	retType = ""
	const = False
	retRank = None
	name = ""

	def __init__(self, m, v):
		self.visibility = v
		self.retType = m.group(1)
		if m.group(2) != None:
			self.const = True
		self.retRank = m.group(3)
		self.name = m.group(4)

class Method():

	cl = None
	visibility = "private"
	virtual = False
	retType = None
	retConst = False
	retRank = None
	name = ""
	args = ""
	const = False
	throw = None

	def __init__(self, cl, m, v):
		self.cl = cl
		self.visibility = v
		if m.group(1) != None:
			self.virtual = True
		if m.group(2) == "virtual" and not self.virtual:
			self.virtual = True
		else:
			self.retType = m.group(2)
		if m.group(3) != None:
			self.retConst = True
		self.retRank = m.group(4)
		self.name = m.group(5)
		self.args = m.group(6)
		if m.group(7) != None:
			self.const = True
		self.throw = m.group(8)

	def toGetter(self, var):
		for prop in self.cl.properties:
			p = prop.name.lower().strip('_')
			if var.startswith(p) or p.startswith(var):
				if prop.retRank == "*" and self.retRank != "*":
					ret = "*%s" % prop.name
				else:
					ret = prop.name
				return "\n\treturn (%s);" % ret
		return ""

	def toSetter(self, var):
		for prop in self.cl.properties:
			p = prop.name.lower().strip('_')
			if var.startswith(p) or p.startswith(var):
				m = reg_param.search(self.args)
				if m != None:
					if m.group(2) == "*" and prop.retRank != "*":
						param = "*%s" % m.group(3)
					else:
						param = m.group(3)
					return "\n\t%s = %s;" % (prop.name, param)
		return ""

	def toCpp(self):
		s = ""
		s += self.retType
		if self.retConst:
			s += " const"
		s += "\t\t"
		if self.retRank != None:
			s += self.retRank
		s += self.cl.name
		s += "::"
		s += self.name
		s += '('
		s += self.args
		s += ')'
		if self.const:
			s += " const"
		if self.throw != None:
			s += self.throw
		s += "\n{"
		if self.name.startswith("get"):
			s += self.toGetter(self.name[3:].lower())
		elif self.name.startswith("set") and len(self.args) > 4:
			s += self.toSetter(self.name[3:].lower())
		s += "\n}"
		return s

def test(view):
	classes = view.find_by_selector("meta.class-struct-block.c++")
	name = view.file_name().split('/')[-1]
	className = name.split('.')[0]
	name = name.replace(".cpp", ".hpp")
	print("#include \"%s\"\n" % name)
	for c in classes:
		cl = Class(className, view)
		cl.parse(c)
		print(cl.toCpp())

class JulooTestCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		test(self.view)

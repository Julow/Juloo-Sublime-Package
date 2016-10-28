#!/usr/bin/env python3
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    gen_theme.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/10/29 01:02:56 by juloo             #+#    #+#              #
#    Updated: 2016/10/29 01:20:27 by juloo            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os, sys

def parse_theme(inp):
	scope_name = None
	rules = []
	for line in inp:
		tmp = line.find(';')
		if tmp >= 0:
			line = line[:tmp]
		line = line.rstrip()
		if len(line) == 0:
			continue
		if line.endswith(":"):
			yield scope_name, rules
			scope_name = line[:-1].strip()
			rules = []
			continue
		words = line.split()
		if len(words) != 2:
			raise Exception("Syntax error '%s'" % line)
		rules.append(tuple(words))
	yield scope_name, rules

if __name__ == '__main__':
	try:
		print("""<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
<key>settings</key>
<array>""")
		for scope, rules in parse_theme(sys.stdin):
			print("<dict>")
			if scope != None:
				print("\t<key>scope</key><string>%s</string>" % scope)
			print("\t<key>settings</key><dict>")
			for rule in rules:
				print("\t\t<key>%s</key><string>%s</string>" % rule)
			print("\t</dict>")
			print("</dict>")
		print("</array>\n</dict>\n</plist>")
	except Exception as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

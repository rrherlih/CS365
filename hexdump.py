#! /usr/bin/env python3.4

files = open('npm-debug.log')
contents = files.read()
#" ".join("{:02x}".format(ord(x)) for x in contents)
for x in contents:
	if x%16 != 0:
		print("{:02x}".format(ord(x)), end=' ')
	else:
		print("{:02x}".format(ord(x)))
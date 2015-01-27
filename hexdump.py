#! /usr/bin/env python3.4

files = open('PinndItPin.png')
files = unicode(files, errors='.')
contents = files.read().decode('utf8')
#" ".join("{:02x}".format(ord(x)) for x in contents)

for x in range(len(contents)):
	if ord(x) not in range(32, 127):
		print(00)
	if x%16 != 0:
		print("{:02x}".format(ord(contents[x])), end=' ')
	else:
		print("{:02x}".format(ord(contents[x])))
print()
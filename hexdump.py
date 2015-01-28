#! /usr/bin/env python3.4

files = open('npm-debug.log')
contents = files.read()

numChars = 0
while len(contents) > 0:
	line = contents[0:15]
	contents = contents[16:len(contents)]
	hexValues = ''
	asciiValues = ''
	for x in line:
		hexValues = hexValues + "{:02x}".format(ord(x)) + ' '
		if ord(x) not in range(32, 127):
			asciiValues = asciiValues + '.'
		else:
			asciiValues = asciiValues + x
	if len(hexValues) != 48:
		while len(hexValues) < 48:
			hexValues = hexValues + '   '
	print("{:08x}".format(numChars), end='  ')
	print(hexValues, sep=' ', end='  ')
	print('|' + asciiValues + '|')
	numChars = numChars + 16



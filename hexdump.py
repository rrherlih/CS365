#! /usr/bin/env python3.4

files = open('npm-debug.log')
contents = files.read()
# files = unicode(files, errors='.')
# contents = files.read().decode('utf8')
#" ".join("{:02x}".format(ord(x)) for x in contents)

for x in range(len(contents)):
	# if ord(x) not in range(32, 127):
	# 	print(00)
	if x%16 == 15:
		print("{:02x}".format(ord(contents[x])))
	elif x%16 == 0:
		print("{:08x}".format(x) + ' ' + "{:02x}".format(ord(contents[x])), end=' ')		
	else:
		print("{:02x}".format(ord(contents[x])), end=' ')
print()


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
	print("{:08x}".format(numChars), end='  ')
	print(hexValues, sep=' ', end='  ')
	print('|' + asciiValues + '|')
	print()
	numChars = numChars + 16



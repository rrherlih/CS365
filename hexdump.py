#! /usr/bin/env python3.4

# files = open('npm-debug.log')
# contents = files.read()

# numChars = 0
# while len(contents) > 0:
# 	line = contents[0:15]
# 	contents = contents[16:len(contents)]
# 	hexValues = ''
# 	asciiValues = ''
# 	for x in line:
# 		hexValues = hexValues + "{:02x}".format(ord(x)) + ' '
# 		if ord(x) not in range(32, 127):
# 			asciiValues = asciiValues + '.'
# 		else:
# 			asciiValues = asciiValues + x
# 	if len(hexValues) != 48:
# 		while len(hexValues) < 48:
# 			hexValues = hexValues + '   '
# 	print("{:08x}".format(numChars), end='  ')
# 	print(hexValues, sep=' ', end='  ')
# 	print('|' + asciiValues + '|')
# 	numChars = numChars + 16


with open('npm-debug.log', 'rb') as f:
	numBytes = 0
	while True:
		line = f.read(16)
		if not line:
			break
		print("{:08x}".format(numBytes), end='  ')
		for x in line:
			print("{:02x}".format(x), end=' ')
			numBytes = numBytes + 1
		print('   '*(16-len(line)), end='')
		print("{: >2}".format('|'), end='')
		for x in line:
			if x not in range(32, 127):
				print('.', end='')
			else:
				print(chr(x), end='')
		print('|')
	print("{:08x}".format(numBytes))
		
		
		



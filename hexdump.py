#! /usr/bin/env python3.4

import sys

with open(sys.argv[1], 'rb') as f:
	numBytes = 0
	while True:
		try:
			line = f.read(16)
		except:
			print(sys.exc_info()[0])
		if not line:
			break
		print("{:08x}".format(numBytes), end='  ')
		try:
			for x in line:
				print("{:02x}".format(x), end=' ')
				numBytes = numBytes + 1
		except:
			print(sys.exc_info()[0])
		print('   '*(16-len(line)), end='')
		print(' |', end='')
		try:
			for x in line:
				if x not in range(32, 127):
					print('.', end='')
				else:
					print(chr(x), end='')
		except:
			print(sys.exc_info()[0])
		print('|')
	print("{:08x}".format(numBytes))
		
		
		



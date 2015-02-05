#! /usr/bin/env python3.4

import sys

class Strings:

	def __init__(self, min_len, input_file):
		self.min_len = min_len
		self.input_file = input_file

	def len_check(self, l):
		if len(l) < self.min_len:
			return False
		else:
			return True

	def open_file(self):
		pass
		

	def strings(self):

		str_text = ''

		try:
			f = open(self.input_file, 'rb')
		except:
			print('Couldn\'t open the file')
			print(sys.exc_info()[0])
			sys.exit()
	
		try:
			line = f.read(16)
		except:
			print('Error reading file')
			print(sys.exc_info()[0])
		
		while line:
			for x in line:
				if x in range(32, 127) or x == 10:
					str_text += chr(x)
				else:
					if self.len_check(str_text):
						print(str_text)
						str_text = ''
					else:
						str_text = ''
				
			try:
				line = f.read(16)
			except:
				print('Error reading file')
				print(sys.exc_info()[0])

		if self.len_check(str_text):
			print(str_text)
			str_text = ''

	def lil_endian(self):
		pass
		# f = open(self.input_file, 'rb')
		# line = f.read(16)
		# while line:
		# 	for x in line:


def main():
	if len(sys.argv) == 3:
		try:
			x = int(sys.argv[1])
		except:
			print('The second argument needs to be a positive integer')
			sys.exit()
		if x < 0:
			print('The second argument needs to be a positive integer')
			sys.exit()
		s = Strings(int(sys.argv[1]), sys.argv[2])
		s.strings()
	else:
		print("Type a minimum string length then the filename")
		sys.exit()

if __name__ == '__main__':
    main()

		
		



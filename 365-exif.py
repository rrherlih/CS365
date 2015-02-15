#!/usr/bin/env python3
"""
Ryan Herlihy
CS365: Digital Forensics, Spring 2015
"""

import sys
from struct import unpack

class UnpackJPEG:

	def open_file(self):
		try:
			self.fd = open(sys.argv[1], 'rb')
		except:
			print("Error opening the file")
			sys.exit()

	def read_file(self):
		try:
			self.data = self.fd.read()
			self.fd.close()
		except:
			print("Error reading the file")
			sys.exit()

	def check_JPEG(self):
		try:
			jpeg_header = unpack(">2B", self.data[0:2])
		except:
			print("Error unpacking bytes")
			sys.exit()
		if jpeg_header == (255, 216):
			print("This is a JPEG image!")
		else:
			print("This is NOT a JPEG!")
			sys.exit()

	def find_markers(self):
		mark_array = []
		index_array = []
		index = 2
		
		while True:
			marker = unpack(">BBH", self.data[index:index+4])
			if "{:02x}".format(marker[1]) == 'da':
				mark_array.append(marker)
				index_array.append(index)
				break
			else:
				mark_array.append(marker)
				index_array.append(index)
				index = index + marker[2] + 2
		
		count = 0
		while count < len(mark_array):
			print("{:#06x}".format(index_array[count]), end=' ')
			print("Marker", end=' ')
			print(hex(mark_array[count][0]) + "{:02x}".format(mark_array[count][1]), end=' ')
			print("size=" + "{:#06x}".format(mark_array[count][2]))
			count += 1

		# print(self.data[2:4].decode("utf-8", "ignore"))

		for i in index_array:
			# exif_check = bytes.decode(self.data[i+4:i+10])
			exif_check = self.data[i+4:i+14].decode("utf-8", "ignore")
			if (exif_check[0:4] == 'Exif'):
				if (exif_check[6:8] != 'MM'):
					sys.exit()
				else:
					print("BIG ENDIAN")
				



	def exif(self):
		self.open_file()
		self.read_file()
		self.check_JPEG()
		self.find_markers()


def main():
  	if len(sys.argv) == 2:
  		uj = UnpackJPEG()
  		uj.exif()
  	else:
  		print("Your command should have two arguments: The program name then the filename")
  
if __name__ == '__main__':
    main()
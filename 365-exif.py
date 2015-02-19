#!/usr/bin/env python3
"""
Ryan Herlihy
CS365: Digital Forensics, Spring 2015
"""

import sys
from struct import unpack

class UnpackJPEG:

	def open_file(self):

		"""
		Opens the file given as an argument into self.fd.
		Exits if issue opening the file.
		"""

		try:
			self.fd = open(sys.argv[1], 'rb')
		except:
			print("Error opening the file")
			sys.exit()

	def check_JPEG(self):

		"""
		Checks if the file is a jpeg by reading the first 2 bytes
		and making sure they are ffd8.
		Exits if it isn't a jpeg.
		"""

		try:
			jpeg_header = self.fd.read(2)
		except:
			print("Error unpacking bytes")
			sys.exit()
		if jpeg_header == b'\xff\xd8':
			print("This is a JPEG image!")
		else:
			print("This is NOT a JPEG!")
			sys.exit()
				
	def find_markers(self):

		"""
		A while loop reads in and unpacks 2 bytes and a short retrieving the marker
		and the marker length. It prepends the index of the marker in the 
		file to the unpacked tuple. This tuple is appended to mark_array. The
		while loop stops when the last marker is unpacked. A for loop then prints
		out the marker index, the marker number, and its length.
		"""

		self.mark_array = []
		index = 2
		
		while True:
			marker = unpack(">BBH", self.fd.read(4))
			marker = (index, ) + marker
			self.mark_array.append(marker)
			if "{:02x}".format(marker[2]) == 'da':
				break
			else:
				index = self.fd.tell() + marker[3] - 2
				self.fd.seek(index)
		
		for m in self.mark_array:
			print("{:#06x}".format(m[0]), end=' ')
			print("Marker", end=' ')
			print(hex(m[1]) + "{:02x}".format(m[2]), end=' ')
			print("size=" + "{:#06x}".format(m[3]))
		

	def find_exif(self):

		"""
		For each marker in mark_array, it seeks to the marker's index then reads
		in 6 bytes. It then checks to see if the Exif header is in those bytes.
		If not the program exits. If it is, the program reads in 2 more bytes
		looking for 'MM' to check if the block is big endian. If not the program
		exits. If it is, 4 bytes are unpacked to get the offset of the ifd tags.
		The position of the start of the ifds are calculated and is seeked to.
		Now that the marker containing the Exif tag is found, the for loop quits.
		Lastly, a short is unpacked to get the number of ifd tags, and then 
		prints that number.
		"""

		self.ifd_start = 0

		for m in self.mark_array:
			self.fd.seek(m[0]+4)
			exif_check = self.fd.read(6)

			if (exif_check[0:4] == b'Exif'):

				"""This line keeps track of where this byte is in the file."""
				self.endian_mark = self.fd.tell()

				if (self.fd.read(2) != b'MM'):
					print("This is a Little Endian Exif block.")
					self.fd.close()
					sys.exit()
				else:
					self.fd.read(2)
					ifd_offset = unpack(">L", self.fd.read(4))
					self.ifd_start = self.fd.tell() + ifd_offset[0] - 8
					self.fd.seek(self.ifd_start)
					break

		if (self.ifd_start == 0):
			print("Error finding Exif header.")
			self.fd.close()
			sys.exit()	

		self.ifd_entries = unpack(">H", self.fd.read(2))[0]
		print("Number of IDF entries:", self.ifd_entries)

	def find_ifds(self):

		"""
		A for loop, reads in and unpacks bytes for each ifd tag until all
		ifd tags are read. Every byte chunk for a tag is put into one tuple 
		then appended to self.ifd_array. Another for loop, loops through
		ifd_array printing out the tag name in hex and string, and then the
		data. If the length of the data is less than 4, the 4th element in the
		tuple is printed as the data. If it is greater than 4, the offset is
		calculated by adding the 4th element of the tuple to the endian_mark
		variable we saved earlier. This index is seeked to and the length of the
		data is read in and printed out.
		"""

		self.ifd_array = []
		bytes_per_component = (0, 1, 1, 2, 4, 8, 1, 1, 2, 4, 8, 4, 8)

		"""For loop puts ifd tags into array as tuples.
		   Each ifd tuple consists of: 
		   (tag, format, # of components, data/data offset, data length)"""
		for x in range(0, self.ifd_entries):
			ifd_info = unpack(">H", self.fd.read(2))			
			ifd_info = ifd_info + unpack(">H", self.fd.read(2))
			ifd_info = ifd_info + unpack(">L", self.fd.read(4))
			ifd_info = ifd_info + unpack(">L", self.fd.read(4))

			"""This last tuple element is calculated by using the format of the ifd_info
			   as the index in the bytes_per_component list, then multiplying it by the
			   number of components."""
			ifd_info = ifd_info + (bytes_per_component[ifd_info[1]] * ifd_info[2],)
			self.ifd_array.append(ifd_info)

		for i in self.ifd_array:
			tag_name = "{:#06x}".format(i[0])
			print(tag_name, "{:<20}".format(self.tag_dict(tag_name)), ':', end=' ')
			if (i[4] <= 4):
				x = bytes(i[4])
				if (i[1] == 1):
					print(i[3])
				elif (i[1] == 2):
					print(i[3])
				elif (i[1] == 3):
					print(i[3])
				elif (i[1] == 4):
					print(i[3])
				elif (i[1] == 5):
					print(i[3])
				elif (i[1] == 7):
					print(i[3])
			else:
				self.fd.seek(self.endian_mark + i[3])
				if (i[1] == 1):
					print(unpack(">B", self.fd.read(i[4][0:1])))
				elif (i[1] == 2):
					print(bytes.decode(self.fd.read(i[4])))
				elif (i[1] == 3):
					print(unpack(">%dH" % i[2], self.fd.read(i[4])))
				elif (i[1] == 4):
					print(unpack(">L", self.fd.read(i[4][0:4])))
				elif (i[1] == 5):
					(num, denom) = unpack(">LL", self.fd.read(i[4]))
					print('[\'', num, '/', denom, '\']', sep='')
				elif (i[1] == 7):
					print(7)
					unpack(">%dB" % i[4], self.fd.read(i[4]))
					print("".join("%c" % x for x in value))
					

		self.fd.close()
			

	def tag_dict(self, tag_hex):

		"""This takes in a hex value and returns the corresponding IFD tag in string form.
		"""

		if tag_hex == '0x010e':
			return 'Image Description'
		elif tag_hex == '0x010f':
			return 'Make'
		elif tag_hex == '0x0110':
			return 'Model'
		elif tag_hex == '0x0112':
			return 'Orientation'
		elif tag_hex == '0x011a':
			return 'X Resolution'
		elif tag_hex == '0x011b':
			return 'Y Resolution'
		elif tag_hex == '0x0128':
			return 'Resolution Unit'
		elif tag_hex == '0x0131':
			return 'Software'
		elif tag_hex == '0x0132':
			return 'DateTime'
		elif tag_hex == '0x013e':
			return 'WhitePoint'
		elif tag_hex == '0x013f':
			return 'Primary Chromaticities'
		elif tag_hex == '0x8298':
			return 'Copyright'
		elif tag_hex == '0x8825':
			return 'GPSInfoIFD'	
		else:
			return 'Unavailable'


	def exif(self):

		"""Runs all the functions in order.
		"""

		self.open_file()
		self.check_JPEG()
		self.find_markers()
		self.find_exif()
		self.find_ifds()


def main():

	"""Checks the correct number of arguments. If correct, UnpackJPEG class is created.
	   The class runs the exif() function.
	"""

	if (len(sys.argv) == 2):
		uj = UnpackJPEG()
		uj.exif()
	else:
		print("Your command should have two arguments: The program name then the filename")
  
if __name__ == '__main__':
    main()
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
		self.ifd_start = 0
		for m in self.mark_array:
			self.fd.seek(m[0]+4)
			exif_check = self.fd.read(6)
			if (exif_check[0:4] == b'Exif'):
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

		self.ifd_entries = unpack(">H", self.fd.read(2))[0]
		print("Number of IDF entries:", self.ifd_entries)

	def find_ifds(self):
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
			ifd_info = ifd_info + (bytes_per_component[ifd_info[1]] * ifd_info[2],)
			self.ifd_array.append(ifd_info)

		for i in self.ifd_array:
			tag_name = "{:#06x}".format(i[0])
			print(tag_name, "{:<20}".format(self.tag_dict(tag_name)), ':', end=' ')
			if (i[4] <= 4):
				print(i[3])
			else:
				self.fd.seek(self.endian_mark + i[3])
				ifd_data = self.fd.read(i[4])
				print(bytes.decode(ifd_data))

	def tag_dict(self, tag_hex):
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
		else:
			return 'Unavailable'


	def exif(self):
		self.open_file()
		# self.read_file()
		self.check_JPEG()
		self.find_markers()
		self.find_exif()
		self.find_ifds()


def main():
  	if len(sys.argv) == 2:
  		uj = UnpackJPEG()
  		uj.exif()
  	else:
  		print("Your command should have two arguments: The program name then the filename")
  
if __name__ == '__main__':
    main()
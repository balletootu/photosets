#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyexiv2 as ev
import os, time, math

def modifyDate(imgPath, date):
	print(imgPath)
	try:
		exiv_image = ev.ImageMetadata(imgPath)
		exiv_image.read()
		# exiv_image["Exif.Image.Artist"] = self.Artist
		exiv_image["Exif.Photo.DateTimeOriginal"] = date#time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(time.time()))
		# exiv_image["Exif.Image.Software"] = self.Software
		exiv_image.write()
		print('ok')
	except:
		print('error')

if __name__ == '__main__':
	now = time.strftime('%Y:%m:%d %H', time.localtime(time.time()))
	for parent, dirnames, filenames in os.walk(r'C:\CodeLib\adultphotosets\cartoon\[白ぅ～凪ぃ] 聖天使ユミエル エンドレスフィード[170P]'.decode('utf-8')):
		for filename in filenames:
			if filename.endswith('jpg'):
				a = int(filename.split('.')[0].split('-')[0])
				second = a % 60
				minute = math.floor(a / 60)
				# print '%s:%02d:%02d' % (now, minute, second)
				modifyDate(os.path.join(parent, filename), '%s:%02d:%02d' % (now, minute, second))
	# print time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(time.time()))
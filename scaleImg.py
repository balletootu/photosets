#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Image, os

def scale(imgPath):
	# 打开一个jpg图像文件，注意路径要改成你自己的:
	print('try to open file: %s' % imgPath)
	im = Image.open(imgPath)
	# 获得图像尺寸:
	w, h = im.size
	if w > 5000 or h > 5000 or True:
		# 缩放到50%:
		im.thumbnail((w // 2, h // 2))
		# 把缩放后的图像用jpeg格式保存:
		arr = imgPath.split('.')
		arr.insert(-1, 's')
		im.save('.'.join(arr), 'jpeg')
		print('saved => %s' % '.'.join(arr))

if __name__ == '__main__':
	for parent, dirnames, filenames in os.walk(r'G:\adultphotosets\imgs\Hegre-Art – Anaya – sunshine'.decode('utf-8')):
		for filename in filenames:
			if filename.endswith('jpg'):
				scale(os.path.join(parent, filename))
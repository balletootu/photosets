#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 生成缩略图，以供上传到qq群文件里

import Image, os, helper

dir_name = r'G:\adultphotosets\imgs\EternalDesire – Abril C – Turgues'.decode('utf-8')


def scale(imgPath):
	print('try to open file: %s' % imgPath)
	im = Image.open(imgPath)
	# 获得图像尺寸:
	w, h = im.size
	im.thumbnail((200, int(h * 200 / w)))
	# 把缩放后的图像用jpeg格式保存:
	arr = imgPath.split('\\')
	arr.insert(-1, 's')
	im.save('\\'.join(arr), 'jpeg')
	print('saved => %s' % '\\'.join(arr))

if __name__ == '__main__':
	helper.mkDir(os.path.join(dir_name, 's'))
	for parent, dirnames, filenames in os.walk(dir_name):
		for filename in filenames:
			if not parent.endswith('\\s'):
				if filename.endswith('jpg'):
					scale(os.path.join(parent, filename))
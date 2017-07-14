#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 下载http://aiss8.com/的图片
import helper
import re, os

def fetchAlbum(url):
	pq = helper.get(url)
	dirName = os.path.join('.', 'aiss', pq('title').text())
	helper.mkDir(dirName)
	index = 1
	for img in pq('.message > img'):
		helper.downloadImg(img.get('src'), os.path.join(dirName, '%03d.jpg' % index))
		index += 1

if __name__ == '__main__':
	page = 1
	while True:
		url = 'http://www.aiss8.com/forum-2-%d.htm' % page
		pq = helper.get(url)
		aArr = pq('a.product-title')
		if aArr and len(aArr) > 0:
			print('now page => %d' % page)
			for a in aArr:
				fetchAlbum('http://www.aiss8.com/%s' % a.get('href'))
		else:
			break
		page += 1
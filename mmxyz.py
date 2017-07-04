#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 下载http://www.mmxyz.net/的图片

import helper
import re, os, calendar, datetime

# http://www.mmxyz.net/?action=ajax_post&pag=1
BASE_URL = 'http://www.mmxyz.net'

def fetchAlbum(url, dirName):
	if 'rosi' in url:
		pq = helper.get(url)
		dirName = os.path.join(dirName, pq('#post-title').text().split('No.')[1])
		helper.mkDir(dirName)
		for a in pq('.gallery-icon > a'):
			imgUrl = a.get('href')
			helper.downloadImg(imgUrl, os.path.join(dirName, imgUrl.split('/')[-1]))


if __name__ == '__main__':
	dirName = 'ROSI写真'
	helper.mkDir(dirName)
	page = 6
	while True:
		pageUrl = '%s/?action=ajax_post&pag=%d' % (BASE_URL, page)
		pq = None
		try:
			pq = helper.get(pageUrl)
		except Exception as e:
			print('something wrong!')
			break
		if pq:
			for a in pq('a.inimg'):
				fetchAlbum(a.get('href'), dirName)
			page += 1

# 			download image: http://img1.mmxyz.net/2016/04/rosi-1594-046.jpg
# download image: http://img1.mmxyz.net/2016/04/rosi-1594-047.jpg
# download image: http://img1.mmxyz.net/2016/04/rosi-1594-048.jpg
# download image: http://img1.mmxyz.net/2016/04/rosi-1594-049.jpg
# download image: http://img1.mmxyz.net/2016/04/rosi-1594-050.jpg
# download image: http://img1.mmxyz.net/2016/04/rosi-1594-051.jpg
# download image: http://img1.mmxyz.net/2016/04/rosi-1594-052.jpg
# get url => http://www.mmxyz.net/rosi-sj-044/
# Traceback (most recent call last):
#   File "mmxyz.py", line 36, in <module>
#     fetchAlbum(a.get('href'), dirName)
#   File "mmxyz.py", line 15, in fetchAlbum
#     dirName = os.path.join(dirName, pq('#post-title').text().split('No.')[1])
# IndexError: list index out of range
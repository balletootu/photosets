#!/usr/bin/env python
# -*- coding: utf-8 -*-

import helper
import os, Queue, threading

BASE_URL = 'http://www.177picxx.info/html/category/tt'

def fetchGallery(url, title, cartoonPage, page = 1, urlArr = None):
	print('now cartoonPage => %d' % cartoonPage)
	print('now cartoon => %s' % title)
	if not urlArr:
		urlArr = []
	pq = helper.get('%s/%d' % (url, page))
	if not pq:
		return False
	for img in pq('p>img'):
		src = img.get('src')
		if src in urlArr:
			dirName = os.path.join('cartoon', title)
			helper.writeFile('\n'.join(urlArr), u'%s/url.txt' % dirName)
			return True
		urlArr.append(src)
	return fetchGallery(url, title, cartoonPage, page + 1, urlArr)

def fetchPage(page):
	url = '%s/page/%d/' % (BASE_URL, page)
	pq = helper.get(url)
	for a in pq('a.disp_a'):
		title =  a.get('title').replace('Permalink to ', '')
		url = a.get('href')
		dirName = os.path.join('cartoon', title)
		if not os.path.exists(os.path.join(dirName, 'url.txt')):
			helper.mkDir(dirName)
			if not fetchGallery(url, title, page):
				return False
	return True

if __name__ == '__main__':
	for page in xrange(1, 224):
		if not fetchPage(page):
			break
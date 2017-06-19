#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 下载http://18h.animezilla.com/manga的漫画

import helper, requests
import re, os, time

headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Host': 'm.iprox.xyz',
	# 'Connection': 'keep-alive',
	# 'Host': '164.94201314.net',
	# 'Referer': 'http://www.hhssee.com/page128374/6.html?s=12&d=0',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.2552.881'
}

# Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
# Accept-Encoding:gzip, deflate, sdch
# Accept-Language:zh-CN,zh;q=0.8
# Cache-Control:max-age=0
# Host:m.iprox.xyz
# If-None-Match:"5de76098c8b583f85ecd2ff8d1f11c63b21a653e"
# Proxy-Connection:keep-alive
# Referer:http://18h.animezilla.com/manga/2408
# Upgrade-Insecure-Requests:1
# User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.2552.888

# 开始下载图片
def downloadImg(url, imgPath, referer):
	if os.path.exists(imgPath):
		print(u'跳过已存在图片:%s' % imgPath)
	else:
		print(u'开始下载图片:%s' % url)
		try:
			global headers
			headers['Referer'] = referer
			r = requests.get(url, stream = True, headers = headers, cookies = {})
		except Exception as e:
			print(e)
			return
		with open(imgPath, 'wb') as f:
			for chunk in r.iter_content(chunk_size = 1024): 
				if chunk:
					f.write(chunk)
					f.flush()

def fetchComic(webPage, comicIndex, url, page = 1, comicDir = None):
	pq = helper.get('%s/%d' % (url, page))
	if page == 1:
		title = pq('title').text().replace('/', '&').split(' - ')[0]
		comicDir = os.path.join('animezilla', title)
		if os.path.exists(os.path.join('animezilla', '0uploaded', title, 'done.txt')):
			return True
		if os.path.exists(os.path.join(comicDir, 'done.txt')):
			return True
		helper.mkDir(comicDir)
	if webPage == 1 and comicIndex == 16:
		if page < 90:
			return fetchComic(webPage, comicIndex, url, 90, comicDir)

	img = pq('img#comic')
	print('[%s] downloading webPage page => %d, comic index => %d, comic page => %d' % (helper.now(), webPage, comicIndex, page))
	downloadImg(img.attr('src'), os.path.join(comicDir, '%03d.jpg' % page), url)
	time.sleep(3)
	if(len(img.parents('a')) == 0):
		helper.writeFile('done', os.path.join(comicDir, 'done.txt'))
		return True
	return fetchComic(webPage, comicIndex, url, page + 1, comicDir)

if __name__ == '__main__':
	goon = True
	for page in range(1, 10):
		url = 'http://18h.animezilla.com/manga/page/%d' % page
		pq = helper.get(url)
		comicIndex = 0
		for a in pq('div.pure-u-2-5 > a'):
			if not fetchComic(page, comicIndex, a.get('href')):
				goon = False
				break
			comicIndex += 1
		if not goon:
			break
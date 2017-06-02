#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 下载http://www.hhssee.com的漫画

import helper, requests
import re, os, time

headers = {
	'Accept': 'image/webp,image/*,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	# 'Connection': 'keep-alive',
	'Host': '164.94201314.net',
	'Referer': 'http://www.hhssee.com/page128374/6.html?s=12&d=0',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.2552.881'
}

def getImgName(pq):
	img = pq('#img1021') or pq('#img2391') or pq('#img7652') or pq('#imgCurr')
	if img:
		return img.attr('name')

def unsuan(s):
	sw = "hhssee.com|9eden.com"
	su = 'www.hhssee.com'
	b = False
	a = sw.split('|')
	for i in a:
		if su.find(i) > -1:
			b = True
			break
	if not b:
		return ''
	x = s[-1]
	xi = "abcdefghijklmnopqrstuvwxyz".find(x) + 1
	sk = s[len(s) - xi - 12 : len(s) - xi - 1]
	s = s[0 : len(s) - xi - 12]
	k = sk[0 : len(sk) - 1]
	f = sk[-1]
	for i in range(0, len(k)):
		s = re.compile(k[i : i + 1]).sub(str(i), s)
	ss = s.split(f)
	s = ''
	for i in range(0, len(ss)):
		s += chr(int(ss[i]))
	return s


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

if __name__ == '__main__':
	baseUrl = 'http://www.hhssee.com'
	pageName = 'page245343'
	for page in range(1, 22):
		url = '%s/%s/%d.html?s=6&d=0' % (baseUrl, pageName, page)
		pq = helper.get(url)
		imgName = getImgName(pq)
		imgUrl = 'http://164.94201314.net/dm06%s' % unsuan(imgName)
		downloadImg(imgUrl, 'hhssee/妄想老师/029/%03d.jpg' % page, url)
		time.sleep(3)
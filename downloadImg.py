#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, requests

headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36 OPR/45.0.2552.635',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'zh-CN,zh;q=0.8'
}

cookies = {
	'__cfduid': '=d260ad47b62c80b296a84fb2bd88970a01488250634',
	'__utma': '234750214.398156472.1488250879.1495090497.1495096934.14',
	'__utmc': '=234750214',
	'__utmz': '234750214.1495096934.14.7.utmcsr=adultphotosets.ru|utmccn=(referral)|utmcmd=referral|utmcct=/hegre-art-milla-introduction/'
}

# 开始下载图片
def downloadImg(url, imgPath):
	if os.path.exists(imgPath):
		print(u'跳过已存在图片:%s' % imgPath)
	else:
		print(u'开始下载图片:%s' % url)
		try:
			global headers
			global cookies
			r = requests.get(url, stream = True, headers = headers, cookies = cookies)
		except Exception, e:
			print(e)
			return
		with open(imgPath, 'wb') as f:
			for chunk in r.iter_content(chunk_size = 1024): 
				if chunk:
					f.write(chunk)
					f.flush()
		# data = urllib.urlopen(url).read()
		# f = file(imgPath, 'wb')
		# f.write(data)
		# f.close()

if __name__ == '__main__':
	# for parent, dirnames, filenames in os.walk(r'G:\adultphotosets\imgs\Hegre-Art – Eden – Unspoilt'.decode('utf-8')):
	f = open(r'G:\adultphotosets\imgs\0error\AvErotica – Cecelia – Heaven\url.txt'.decode('utf-8'))
	urlArr = f.read()
	f.close()

	urlArr = urlArr.split('\n')
	for url in urlArr:
		imgName = url.split('/')[-1]
		downloadImg(url, r'G:\adultphotosets\imgs\0error\AvErotica – Cecelia – Heaven\%s'.decode('utf-8') % imgName)
		break
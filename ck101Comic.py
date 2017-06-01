#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 下载http://comic.ck101.com的漫画

import helper, requests
import re, os

headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Cache-Control': 'max-age=0',
	'Host': 'comic.ck101.com',
	'Proxy-Connection': 'keep-alive',
	'Referer': 'http://comic.ck101.com/vols/8176348/6',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36 OPR/45.0.2552.812'
}

cookies = {
	'__cfduid': 'd8132fabd4f8583e38b6c19bc60f3a64b1495715023',
	'__asc': '6f5adc7715c3f8ff5158ac59087',
	'__auc': '6f5adc7715c3f8ff5158ac59087',
	'__utmt': '1',
	'__utma': '159540015.1744335368.1495715018.1495715018.1495715018.1',
	'__utmb': '159540015.1.10.1495715018',
	'__utmc': '159540015',
	'__utmz': '159540015.1495715018.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
}

if __name__ == '__main__':
	# baseUrl = 'http://comic.ck101.com/vols/8176348'
	baseUrl = 'http://www.qqmanga.com/vols/8176348/1'
	page = 7
	# pq = helper.get('%s/%d' % (baseUrl, page), cookies, headers)
	# print(pq('img#defualtPagePic'))

	response = requests.get('%s/%d' % (baseUrl, page), headers = headers, cookies = cookies)
	if response.status_code == 200:
		pq = PyQuery(response.text)
	else:
		print("error")

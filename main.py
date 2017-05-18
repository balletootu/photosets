#!/usr/bin/env python
# -*- coding: utf-8 -*-

import helper
import re, os, Queue, threading

BASE_URL = 'http://adultphotosets.ru'

def fetchLargeImageUrl(imgUrl):
	if not imgUrl.endswith('zip'):
		if 'imagehosting.pro' in imgUrl or 'gif-jpg.com' in imgUrl or 'ipics.info' in imgUrl:
			pq = helper.get(imgUrl)
			img = pq('img.centred')
			url = img.attr('src')
			if not url:
				img = pq('img.centred_resized')
				url = img.attr('src')
			if url == None:
				return ''
			return url
		elif 'img.yt' in imgUrl or 'imgcandy.net' in imgUrl:
			if 'img.yt' in imgUrl:
				imgUrl = imgUrl.replace('http:', 'https:')
			pq = helper.post(imgUrl)
			img = pq('img.centred')
			return img.attr('src')
		elif 'imgchili.net' in imgUrl:
			# global imgchili_cookies
			# pq = helper.get(imgUrl, imgchili_cookies)
			# img = pq('img#show_image')
			# url = img.attr('src')
			# return url
			
			# http://imgchili.net/show/102747/102747596__sexart_raddia_cover.jpg
			# http://i11.imgchili.net/102747/102747596__sexart_raddia_cover.jpg
			url = imgUrl.replace('//imgchili', '//i11.imgchili').replace('show/', '')
			return url
		elif 'imagetwist.com' in imgUrl:
			pq = helper.get(imgUrl)
			if not pq:
				return ''
			img = pq('img.img-responsive')
			url = img.attr('src')
			return url
		elif 'dfiles.ru' in imgUrl:
			# 这是个提供下载zip的页面，直接跳过
			return ''
		elif 'imgtrex.com' in imgUrl:
			pq = helper.get(imgUrl)
			img = pq('img.pic')
			return img.attr('src')
		elif 'addimage.info' in imgUrl:
			print('addimage.info is over!!!')
			return ''
		else:
			print('unknow image url => %s' % imgUrl)
			return None
	return ''

def fetchGallery(url, page):
	print('now page %d' % page)
	pq = helper.get(url)
	# SexArt – Alexis Crystal & Michael Fly – Call | AdultPhotoSets.ru
	title = pq('title').text()
	title = title.split(' | ')[0]
	dirName = os.path.join('imgs', '0uploaded', title)
	if os.path.exists(dirName):
		print('exists!!! skip!')
		return True
	dirName = os.path.join('imgs', '0uploaded', '0baidu', title)
	if os.path.exists(dirName):
		print('exists!!! skip!')
		return True

	dirName = os.path.join('imgs', '0error', title)
	if os.path.exists(dirName):
		print('exists!!! skip!')
		return True

	# 创建本地目录
	dirName = os.path.join('imgs', title)
	# print('make dir %s' % dirName)
	# 如果存在url.txt，说明这个相册已经抓取过了，直接return吧
	if os.path.exists('%s/url.txt' % dirName):
		print('exists!!! skip!')
		return True
	helper.mkDir(dirName)
	i = 0
	imgUrl = []
	aArr = pq('a.externalLink')
	if not aArr or len(aArr) < 1:
		aArr = pq('div.content>p>a')
		if not aArr or len(aArr) < 1:
			# http://imgtrex.com/8kbfdzphqsr1/daniela-dressed-for-sex-02-10000px
			arr = re.compile(r'http://imgtrex\.com/\w+/[a-z0-9-]+\.jpg').findall(pq.html())
			if len(arr) == 0:
				print('can\'t find any <a>')
				return False
			aArr = [{'href': a} for a in arr]
			# for a in arr:
			# 	aArr.append({'href': a})
	
	for a in aArr:
		print('%s image index => %d' % (helper.now(), i))
		url = fetchLargeImageUrl(a.get('href'))
		if url == None:
			print('fetchLargeImageUrl failed')
			return False
		else:
			if url <> '':
				imgUrl.append(url)
			i += 1
	if len(imgUrl) > 0:
		helper.writeFile('\n'.join(imgUrl), '%s/url.txt' % dirName)
	return True

def fetchPage(page):
	url = '%s/page/%d/' % (BASE_URL, page)
	pq = helper.get(url)
	for a in pq('h2 > a'):
		if not fetchGallery(a.get('href'), page):
			return False
	return True

if __name__ == '__main__':
	# page: 120
	for page in xrange(120, 224):
		if not fetchPage(page):
			break

	# print fetchLargeImageUrl('http://imgtrex.com/1hveh08jcjk7/cover.jpg')
	# 
	# http://i11.imgchili.net/89928/89928089__cindy_beauty_treatment_poste.jpg
	# http://imgchili.net/show/89928/89928089__cindy_beauty_treatment_poste.jpg
	# http://i6.imgchili.net/89928/89928089__cindy_beauty_treatment_poste.jpg
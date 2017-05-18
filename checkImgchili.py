#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 修复imgchili网站的一个bug

import helper
import re, os, Queue, threading
import shutil

def fetchLargeImageUrl(imgUrl, tag):
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
			url = imgUrl.replace('//imgchili', '//i%s.imgchili' % tag).replace('show/', '')
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


def fetchGallery(url):
	pq = helper.get(url)
	# SexArt – Alexis Crystal & Michael Fly – Call | AdultPhotoSets.ru
	title = pq('title').text()
	title = title.split(' | ')[0]
	dirName = os.path.join('imgs', '0error', title)

	i = 0
	tag = None
	imgUrl = []
	aArr = pq('a.externalLink')
	if not aArr or len(aArr) < 1:
		aArr = pq('div.content>p>a')
		if not aArr or len(aArr) < 1:
			# http://imgtrex.com/8kbfdzphqsr1/daniela-dressed-for-sex-02-10000px
			arr = re.compile(r'http://imgtrex\.com/\w+/[a-z0-9-]+\.jpg').findall(pq.html())
			if len(arr) == 0:
				print('can\'t find any <a>')
				return None
			aArr = [{'href': a} for a in arr]
			# for a in arr:
			# 	aArr.append({'href': a})
			
		if aArr and len(aArr) > 0:
			if 'imgchili.net' in aArr[0].get('href'):
				imgArr = pq('div.content>p>a>img')
				# http://t10.imgchili
				tag = imgArr[0].get('src').replace('http://', '').split('.imgchili')[0].replace('t', '')
	print tag
	print '====================================='
	for a in aArr:
		print('%s image index => %d' % (helper.now(), i))
		url = fetchLargeImageUrl(a.get('href'), tag)
		if url == None:
			print('fetchLargeImageUrl failed')
			return None
		else:
			if url <> '':
				imgUrl.append(url)
			i += 1
	if len(imgUrl) > 0:
		helper.writeFile('\n'.join(imgUrl), '%s/url.txt' % dirName)
	return title

# if __name__ == '__main__':
# 	b = False
# 	repaire_file_arr = []
# 	error_dir = os.path.join('imgs', '0error')
# 	for parent, dirnames, filenames in os.walk(error_dir):
# 		# print parent
# 		for filename in filenames:
# 			if filename.endswith('txt'):
# 				url_txt_path = os.path.join(parent, filename)
# 				f = open(url_txt_path)
# 				url_txt = f.read()
# 				f.close()

# 				if 'imgchili' in url_txt:
# 					# repaire_file_arr.append(url_txt_path)
# 					tmpArr = url_txt_path.replace('imgs\\0error\\', '').replace('\\url.txt', '').replace('&', '-').split(' ')
# 					tmpArr1 = []
# 					for ss in tmpArr:
# 						if re.match(r'\w+', ss):
# 							tmpArr1.append(ss)
# 					title = fetchGallery('http://adultphotosets.ru/%s' % '-'.join(tmpArr1))
# 					if title:
# 						print os.path.join('imgs', title)
# 						shutil.move(os.path.join('imgs', '0error', title), os.path.join('imgs', title))
# 						b = True
# 						break
# 		if b :
# 			break


if __name__ == '__main__':
	arr = []
	dirName = os.path.join('imgs')
	for parent, dirNames, fileNames in os.walk(dirName):
		for dirName in dirNames:
			if '0baidu' in parent or '0error' in parent or '0upload' in parent:
				continue
			if dirName == '0baidu' or dirName == '0error' or dirName == '0uploaded':
				continue
			urlTxtPath = os.path.join(parent, dirName, 'url.txt')
			if not os.path.exists(urlTxtPath):
				arr.append(dirName)
			else:
				f = open(urlTxtPath)
				urlTextContent = f.read()
				f.close()
				if 'imgchili' in urlTextContent:
					arr.append(dirName)
	# print arr
	for a in arr:
		print(os.path.join('imgs', a), os.path.join('imgs', '0error', a))
		shutil.move(os.path.join('imgs', a), os.path.join('imgs', '0error', a))
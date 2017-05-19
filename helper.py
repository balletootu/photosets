#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, requests, time
from pyquery import PyQuery

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}

def now(): 
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def today(): 
	return time.strftime('%Y-%m-%d', time.localtime(time.time()))

def mkDir(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return path	

def writeFile(content, path):
	try:
		f = open(path, 'w')
		f.write(content)
		f.close()
		return True
	except Exception as e:
		print(e)
		return False

# 开始下载图片
def downloadImg(url, imgPath):
	if url != None:
		if os.path.exists(imgPath):
			print('%s is exists, jump it!' % imgPath)
		else:
			print('download image: %s' % url)
			try:
				r = requests.get(url, stream = True)
			except Exception as e:
				print(e)
				return
			with open(imgPath, 'wb') as f:
				for chunk in r.iter_content(chunk_size = 1024): 
					if chunk:
						f.write(chunk)
						f.flush()
def get(url, cookies = {}):
	print('get url => ' + url)
	global headers
	response = requests.get(url, headers = headers, cookies = cookies)
	if response.status_code == 200:
		return PyQuery(response.text)
	else:
		return None

def post(url):
	print('post url => ' + url)
	global headers
	response = requests.post(url, headers = headers, cookies = {}, data = {'imgContinue': 'Continue to image ... '})
	if response.status_code == 200:
		return PyQuery(response.text)
	else:
		return None
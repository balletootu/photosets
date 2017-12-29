#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import time
import platform
import datetime
import subprocess
import inspect
from pyquery import PyQuery
from requests.adapters import HTTPAdapter

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
			parent = '/'.join(imgPath.split('/')[: -1])
			mkDir(parent)
			print('[%s] download image: %s' % (now(), url))
			try:
				global headers
				r = requests.get(url, stream=True, headers=headers)
			except Exception as e:
				print(e)
				return
			with open(imgPath, 'wb') as f:
				for chunk in r.iter_content(chunk_size = 1024): 
					if chunk:
						f.write(chunk)
						f.flush()

def get(url, cookies = {}, myHeaders = None, sleep = None, returnText = False):
	s = requests.Session()
	s.mount('http://', HTTPAdapter(max_retries=10))
	s.mount('https://', HTTPAdapter(max_retries=10))
	if sleep:
		time.sleep(sleep)
	print('get url => ' + url)
	global headers

	response = s.get(url, headers=myHeaders or headers, cookies=cookies, timeout=10)
	
	if response.status_code == 200:
		return response.text if returnText else PyQuery(response.text)
	else:
		return None

def post(url, sleep = 0):
	s = requests.Session()
	s.mount('http://', HTTPAdapter(max_retries=10))
	s.mount('https://', HTTPAdapter(max_retries=10))
	if sleep > 0:
		time.sleep(sleep)
	print('post url => ' + url)
	global headers
	response = s.post(url, headers = headers, cookies = {}, data = {'imgContinue': 'Continue to image ... '})
	if response.status_code == 200:
		return PyQuery(response.text)
	else:
		return None

def optimizeImg(imgFile):
	system = platform.system()
	file = os.path.join(os.path.abspath("."), "pingo.exe")
	if (system == "Windows" and os.path.isfile(file)):
		os.system("{} -s5 {}".format(file, imgFile))

def lookUp(obj):
	print(inspect.getmembers(obj, inspect.ismethod))

def getMonth(english):
	'''从英文转成阿拉伯数字'''
	if english == 'Jan':
		return 1
	if english == 'Feb':
		return 2
	if english == 'Mar':
		return 3
	if english == 'Apr':
		return 4
	if english == 'May':
		return 5
	if english == 'Jun':
		return 6
	if english == 'Jul':
		return 7
	if english == 'Aug':
		return 8
	if english == 'Sep':
		return 9
	if english == 'Oct':
		return 10
	if english == 'Nov':
		return 11
	if english == 'Dec':
		return 12
	return english


def runCmd(cmd, logfile='./aria2c.log', timeout=1200):
	process = None
	if logfile:
		process = subprocess.Popen('%s >>%s 2>&1' % (cmd, logfile), shell=True)
	else:
		process = subprocess.Popen(cmd, shell=True)
	# print(u'run cmd => %s' % cmd)
	process.wait()
	start = datetime.datetime.now()
	while process.poll() is None:
		time.sleep(0.1)
		now = datetime.datetime.now()
		if (now - start).seconds > timeout:
			try:
				process.terminate()
			except Exception as e:
				return None
			return None
	out = process.communicate()[0]
	if process.stdin:
		process.stdin.close()
	if process.stdout:
		process.stdout.close()
	if process.stderr:
		process.stderr.close()
	try:
		process.kill()
	except OSError:
		pass
	return out
		

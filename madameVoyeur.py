#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 下载http://madamevoyeur.com/的图片

import helper
import re, os, calendar, datetime

# http://madamevoyeur.com/index.php?p=1&a=2010
BASE_URL = 'http://madamevoyeur.com'

# def fetchImagePage(year, pageIndex):
# 	url = 'http://madamevoyeur.com/index.php?p=365&a=2016'
# 	pq = helper.get(url)
# 	pq("a[name='%s']>video" %CateGory)
# 	for item in pq(paramter):

if __name__ == '__main__':
	dirName = 'madameVoyeur'
	helper.mkDir(dirName)
	t = datetime.datetime.now()
	nowYear = int(t.year)
	year = 2012
	while year <= nowYear:
		pageIndex = 1
		for pageIndex in range(1, calendar.isleap(year) and 367 or 366):
			print('%s => year: %d page: %d' % (helper.now(), year, pageIndex))
			# http://madamevoyeur.com/images/2016/16035.jpg
			helper.downloadImg('%s/images/%d/%02d%03d.jpg' % (BASE_URL, year, 0 if year == 2010 else year - 2000, pageIndex), os.path.join(dirName, '%d_%03d_1.jpg' % (year, pageIndex)))
			helper.downloadImg('%s/images/%d-2/%02d%03d.jpg' % (BASE_URL, year, 0 if year == 2010 else year - 2000, pageIndex), os.path.join(dirName, '%d_%03d_2.jpg' % (year, pageIndex)))
			helper.downloadImg('%s/images/%d-3/%02d%03d.jpg' % (BASE_URL, year, 0 if year == 2010 else year - 2000, pageIndex), os.path.join(dirName, '%d_%03d_3.jpg' % (year, pageIndex)))
		year += 1
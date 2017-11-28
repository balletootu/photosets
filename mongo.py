#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
# 连接NAS数据库，没有则自动创建
db = conn.NAS
# 使用models集合，没有则自动创建
models = db.models
albums = db.albums

# for data in models.find({'name': 'Abril C'}):
#     print data


def newAlbun(name, date):
    global albums
    albums.insert({
        'name': name,
        'date': date
    });
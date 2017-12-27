#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
抓取femjoy网站上的所有model和她的作品
'''
import os
import json
import datetime
import helper

modelArr = []
albumArr = []

# def findModel(id):
#     global modelArr
#     for model in modelArr:
#         if model.get('id') == id:
#             return model

if __name__ == '__main__':
    model_dir = '/Users/eddie104/Documents/hongjie/photosets/femjoy/model'
    helper.mkDir(model_dir)
    page = 1
    while True:
        url = 'https://www.femjoy.com/api/v2/actors?sorting=date&thumb_size=355x475&limit=48&page=%d' % page
        txt = helper.get(url, returnText=True)
        jsonData = json.loads(txt)
        total_pages = jsonData.get('pagination').get('total_pages')

        for modelData in jsonData.get('results'):
            model = {
                'id': modelData.get('id'),
                'slug': modelData.get('slug'),
                'name': modelData.get('name'),
                'img': modelData.get('thumb').get('image'),
                'Height': modelData.get('height'),
                'Weight': modelData.get('weight'),
                'Measurements': '%s/%s/%s' % (modelData.get('chest', '0'), modelData.get('waist', '0'), modelData.get('hip', '0')),
                'Ethnicity': modelData.get('ethnicity')
            }
            modelArr.append(model)
            # 下载头像先
            helper.downloadImg(model.get('img'), os.path.join(
                model_dir, '%s.jpg' % model.get('name')))
            helper.writeFile(json.dumps(model), os.path.join(model_dir, '%s.json' % model.get('name')))
        page += 1
        if page > total_pages:
            break
    
    photo_dir = '/Users/eddie104/Documents/hongjie/photosets/femjoy/photo'
    helper.mkDir(photo_dir)
    for model in modelArr:    
        page = 1
        while True:
            url = 'https://www.femjoy.com/api/v2/actors/%s/galleries?thumb_size=481x642&limit=20&page=%d' % (model.get('slug'), page)
            txt = helper.get(url, returnText=True)
            jsonData = json.loads(txt)
            total_pages = jsonData.get('pagination').get('total_pages')

            for photoData in jsonData.get('results'):
                dateArr = photoData.get('release_date').split(' ')
                dateStr = '%s-%s-%s' % (dateArr[2], helper.getMonth(dateArr[0].replace(',', '')), dateArr[1].replace(',', ''))
                modelNameArr = []
                for actor in photoData.get('actors'):
                    modelNameArr.append(actor.get('name'))
                photo = {
                    'id': photoData.get('id'),
                    'img': photoData.get('thumb').get('image'),
                    'model': modelNameArr,
                    'name': photoData.get('title'),
                    'date': dateStr
                }
                album_dir = os.path.join(photo_dir, '%s_%s' % (dateStr, photo.get('name')))
                helper.mkDir(album_dir)
                helper.downloadImg(photo.get('img'), os.path.join(
                    album_dir, '%s_%s.jpg' % (dateStr, photo.get('name'))))
                helper.writeFile(json.dumps(photo), os.path.join(
                    album_dir, '%s_%s.json' % (dateStr, photo.get('name'))))
            page += 1
            if page > total_pages:
                break

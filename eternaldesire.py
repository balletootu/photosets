#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
抓取eternaldesire网站上的所有model和她的作品
'''

import helper
import os
import json

CHAT_ARR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'V', 'W', 'Y', 'Z']
chatIndex = 0

def fetchModel(url=None, headUrl=None, name= 'Abril C', score=8.97):
    if url is None:
        url = 'https://www.eternaldesire.com/model/abril-c/'
    if headUrl is None:
        headUrl = 'https://static.eternaldesire.com/media/headshots/abril-c.jpg?fv=e6f189022422389d377149f795d1da13'

    modelPath = os.path.join('eternaldesire', 'models', name)
    helper.mkDir(modelPath)
    helper.downloadImg(headUrl, os.path.join(modelPath, '%s_EternalDesire.jpg' % name))

    modelInfo = {
        'name': name,
        'score': score,
        'Age first shot': 0,
        'Eye color': '',
        'Hair color': '',
        'Breasts': '',
        'Shaved': '',
        'Measurements': '',
        'Height': '',
        'Weight': '',
        'Country': '',
        'Ethnicity': '',
        'photos': []
    }
    
    pq = helper.get(url, None, None, 1)
    infoLiArr = pq('.model_info > ul > li')
    for li in infoLiArr:
        arr = li.text_content().split(': ')
        for key in modelInfo:
            if key == arr[0]:
                modelInfo[key] = arr[1]
                break
    photoIndex = 1
    while photoIndex < 100:
        photoDivArr = pq('#latest_photo_update_%d .update_cell' % photoIndex)
        liArr = pq('#latest_photo_update_%d .hover_container_stats li' % photoIndex)
        if not liArr or len(liArr) == 0:
            break
        for i in xrange(0, len(photoDivArr)):
            photoInfo = {
                'name': '',
                'date': '0.0.1970',
                'model': ''
            }
            img = photoDivArr[i].find('a').find('img')
            coverUrl = img.get('src')
            photoInfo['name'] = img.get('alt')
            photoInfo['date'] = liArr[i * 3].text_content().replace('Date published:', '')
            photoInfo['model'] = liArr[i * 3 + 1].text_content().replace('Featuring: ', '')
            jsonStr = json.dumps(photoInfo)
            photoPath = os.path.join('eternaldesire', 'photos', photoInfo.get('name') + '-' + photoInfo['model'])
            helper.mkDir(photoPath)
            helper.writeFile(jsonStr, os.path.join(photoPath, 'info.json'))
            helper.downloadImg(coverUrl, os.path.join(
                               photoPath, '%s_cover_EternalDesire.jpg' % photoInfo.get('name')))

            modelInfo['photos'].append(photoInfo)
        photoIndex += 1
    helper.writeFile(json.dumps(modelInfo), os.path.join(modelPath, 'info.json'))


        # Ethnicity: Caucasian


def main():
    # https://www.eternaldesire.com/models/all/A/
    global chatIndex
    chatIndex = 12
    b = False
    while chatIndex < 23:
        url = 'https://www.eternaldesire.com/models/all/%s/' % CHAT_ARR[chatIndex]
        pq = helper.get(url)
        scoreSpanArr = pq('.update_information_gallery_rating_number')
        aArr = pq('.update_information_model_name')
        imgArr = pq('td > a> img')
        for i in xrange(0, len(imgArr)):
            if imgArr[i].get('alt') == 'Mila':
                b = True
            if b:
                fetchModel(aArr[i].get('href'), imgArr[i].get('src'), imgArr[i].get('alt'), scoreSpanArr[i].text)
            # break
        chatIndex += 1
    
if __name__ == '__main__':
    main()
    # fetchModel()
    
    # https://www.eternaldesire.com/model/nika-n/
    # https://www.metart.com/model/nika-n/

    # https://www.thelifeerotic.com/model/nika-n/
    # https://www.metartx.com/model/nika-n/
    # https://www.vivthomas.com/model/nika-n/
    # https://www.sexart.com/model/nika-n/
    # https://www.eroticbeauty.com/model/adel-morel/
    # https://www.stunning18.com/model/angelina-ballerina/
    # https://www.rylskyart.com/model/lija/
    # https://www.goddessnudes.com/model/emily-bloom/gallery/20140911/EMILY_BLOOM_6/
    # https://www.errotica-archives.com/model/ginger-frost/gallery/20171025/GINGER_FROST/
    # https://www.domai.com/model/ginger-frost/gallery/20171027/GINGER_FROST_5/
    # https://www.rylskyart.com/models/top/

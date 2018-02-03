#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
抓取eroticbeauty网站上的所有model和她的作品
'''
import os
import json
import datetime
import helper
# import mongo

CHAT_ARR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def fetch_model(url, name, head_img):
    '''fetch model'''
    model_dir = os.path.join('eroticbeauty', 'model')
    helper.mkDir(model_dir)
    helper.mkDir(os.path.join('eroticbeauty', 'photo'))
    # 下载头像先
    helper.downloadImg(head_img, os.path.join(model_dir, '%s.jpg' % name))
    if os.path.exists(os.path.join('eroticbeauty', 'model', '%s.json' % (name))):
        return
    # 然后去抓取详细数据
    model_info = {
        'name': name,
        'photos': []
    }
    pyquery = helper.get(url)
    country_span = pyquery('.custom-country')
    model_info['country'] = country_span.text()

    # 获取照片数据
    custom_content_list = pyquery('.custom-content-list')
    custom_content = None
    for item in custom_content_list:
        if item.getchildren()[0].getchildren()[0].text.startswith('Photos with'):
            custom_content = item
            break
        # if item.getchildren()[0].getchildren()[0].text:
        #     pass
    if custom_content is None:
        helper.writeFile(json.dumps(model_info), os.path.join('eroticbeauty', 'model', '%s.json' % (name)))
        return
    list_group_item_list = custom_content.getchildren()[2].findall('li')
    for list_group_item in list_group_item_list:
        custom_list_item_detailed = list_group_item.getchildren()[1]
        img = custom_list_item_detailed.getchildren()[0].getchildren()[0].getchildren()[0]
        photo_name = img.get('alt').replace('/', ' ') # custom_list_item_detailed.getchildren()[1].getchildren()[0].getchildren()[0].text
        # Released: Feb 26, 2016
        date_str = custom_list_item_detailed.getchildren()[1].getchildren()[1].text_content().split(': ')[1]
        date_str = '%s-%d-%s' % (date_str.split(', ')[1], helper.getMonth(date_str.split(' ')[0]), date_str.split(' ')[1].replace(',', ''))
        # 模特名
        arr = custom_list_item_detailed.getchildren()[1].getchildren()[2].getchildren()
        model_name_arr = []
        for i in xrange(1, len(arr)):
            model_name_arr.append(arr[i].text)
        # model_name = custom_list_item_detailed.getchildren()[1].getchildren()[2].getchildren()[1].text
        # print(model_name_arr)
        # date = datetime.datetime(int(date_str.split(', ')[1]), helper.getMonth(date_str.split(' ')[0]), int(date_str.split(' ')[1].replace(',', '')))
        # print date
        # 下载照片的封面
        photo_path = os.path.join('eroticbeauty', 'photo', photo_name, '%s_%s.jpg' % (
            date_str, photo_name))
        helper.downloadImg(img.get('src'), photo_path)
        # 存到数据库
        # mongo.newAlbun(photo_name, date)
        photo_json = {
            'date': date_str,
            'name': photo_name,
            'model': model_name_arr
        }
        photo_json_str = json.dumps(photo_json)
        model_info.get('photos').append(photo_json)
        helper.writeFile(photo_json_str, os.path.join(
            'eroticbeauty', 'photo', photo_name, '%s_%s.json' % (date_str, photo_name)))
    helper.writeFile(json.dumps(model_info), os.path.join('eroticbeauty', 'model', '%s.json' % (name)))

def main(chat_index=0, enabled=False):
    '''main'''
    b = True
    is_enabled = enabled
    if chat_index < 26:
        url = 'https://www.eroticbeauty.com/models/all//%s' % CHAT_ARR[chat_index]
        pyquery = helper.get(url)
        a_arr = pyquery('.list-group-item > a')
        for item in a_arr:
            if b:
                url = item.get('href')
                print('now => %s' % url)
                # if url == "https://www.metart.com/model/uliya-a/":
                #     is_enabled = True
                if is_enabled:
                    head_img = item.find('img').get('src')
                    name = item.find('img').get('alt')
                    json_path = os.path.join(
                        'eroticbeauty', 'model', '%s.json' % name)
                    img_pathh = os.path.join(
                        'eroticbeauty', 'model', '%s.jpg' % name)
                    if not os.path.exists(json_path) or not os.path.exists(img_pathh):
                        fetch_model(url, name, head_img)
                b = False
            else:
                b = True
        main(chat_index + 1, is_enabled)


if __name__ == '__main__':
    main(0, True)
    # fetch_model('https://www.metart.com/model/lorian/', 'Lorian', '')

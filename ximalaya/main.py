# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2019/6/30 12:03
# @File : main.py

import requests
import re
import os

url = 'http://180.153.255.6/mobile/v1/album/track/ts-1571294887744?albumId=23057324&device=android&isAsc=true&isQueryInvitationBrand=true&pageId={}&pageSize=20&pre_page=0'
headers = {'User-Agent': 'Xiaomi'}

def download():
    for i in range(1, 3):
        r = requests.get(url=url.format(i), headers=headers)
        js_data = r.json()
        data_list = js_data.get('data', {}).get('list', [])
        for item in data_list:
            trackName = item.get('title')
            trackName = re.sub('[\/\\\:\*\?\"\<\>\|]', '_', trackName)
            # trackName=re.sub(':','',trackName)
            src_url = item.get('playUrl64')
            filename = '{}.mp3'.format(trackName)
            if not os.path.exists(filename):

                try:
                    r0 = requests.get(src_url, headers=headers)
                except Exception as e:
                    print(e)
                    print(trackName)
                    r0 = requests.get(src_url, headers=headers)


                else:
                    with open(filename, 'wb') as f:
                        f.write(r0.content)

                    print('{} downloaded'.format(trackName))

            else:
                print(f'{filename}已经下载过了')

import shutil

def rename_():
    for i in range(1, 3):
        r = requests.get(url=url.format(i), headers=headers)
        js_data = r.json()
        data_list = js_data.get('data', {}).get('list', [])
        for item in data_list:
            trackName = item.get('title')
            trackName = re.sub('[\/\\\:\*\?\"\<\>\|]', '_', trackName)
            src_url = item.get('playUrl64')

            orderNo=item.get('orderNo')

            filename = '{}.mp3'.format(trackName)
            try:

                if os.path.exists(filename):
                    new_file='{}_{}.mp3'.format(orderNo,trackName)
                    shutil.move(filename,new_file)
            except Exception as e:
                print(e)





if __name__=='__main__':
    rename_()

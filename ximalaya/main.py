# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2019/6/30 12:03
# @File : main.py

import requests
import re
url = 'https://www.ximalaya.com/revision/play/album?albumId=23057324&pageNum=1&sort=1&pageSize=60'
headers={'User-Agent':'Xiaomi'}

r = requests.get(url=url,headers=headers)
js_data = r.json()
data_list = js_data.get('data',{}).get('tracksAudioPlay',[])
for item in data_list:
    trackName=item.get('trackName')
    trackName=re.sub(':','',trackName)
    src_url = item.get('src')
    try:
        r0=requests.get(src_url,headers=headers)
    except Exception as e:
        print(e)
        print(trackName)
    else:
        with open('{}.m4a'.format(trackName),'wb') as f:
            f.write(r0.content)
        print('{} downloaded'.format(trackName))
# -*-coding=utf-8-*-

# @Time : 2019/10/18 18:04
# @File : story.py

# 睡前故事
import os

import requests,datetime,re

url='http://mobwsa.ximalaya.com/mobile-album/album/page/ts-1571392955128?ac=WIFI&albumId=260744&device=android&isAsc=false&isQueryInvitationBrand=true&isVideoAsc=true&pageId={}&pageSize=100&pre_page=0&source=5&supportWebp=true'
headers = {'User-Agent': 'Xiaomi'}

def download():

    for i in range(1, 2): # 只下载一页

        r = requests.get(url=url.format(i), headers=headers)
        js_data = r.json()
        data_list = js_data.get('data', {}).get('tracks',{}).get('list',[])

        for item in data_list:
            trackName = item.get('title')
            trackName = re.sub('[\/\\\:\*\?\"\<\>\|]', '_', trackName)
            # trackName=re.sub(':','',trackName)
            src_url = item.get('playUrl64')
            orderNo = item.get('orderNo')

            filename = '{}-{}.mp3'.format(orderNo,trackName)
            if not os.path.exists(filename):

                try:
                    r0 = requests.get(src_url, headers=headers,timeout=3600)
                except Exception as e:
                    print(e)
                    print(trackName)
                    r0 = requests.get(src_url, headers=headers,timeout=3600)



                with open(filename, 'wb') as f:
                    f.write(r0.content)
                    print('{}下载完成'.format(filename))

            else:
                print(f'{filename}已经下载过了')

if __name__=='__main__':
    print(f'start at {datetime.datetime.now()}')
    download()
    print(f'end at {datetime.datetime.now()}')

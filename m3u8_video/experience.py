# -*-coding=utf-8-*-

# @Time : 2019/12/2 9:17
# @File : experience.py
import requests
url='https://jh0p4t0rh9rs9610ryc.exp.bcevod.com/mda-jjkxjt57fdsith87/mda-jjkxjt57fdsith87.m3u8.{}.ts'
total = 253
headers={'User-Agent':'Xiaomi'}
data = 'data'
for i in range(total+1):
    try:
        r = requests.get(url.format(i),headers=headers)
    except Exception as e:
        print(e)
    else:
        with open('data/{}.ts'.format(i),'wb') as f:
            f.write(r.content)
        print('done {}.ts'.format(i))


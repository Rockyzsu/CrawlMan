# coding: utf-8
import requests
from toolkit import getheader
def spider():
    for i in range(4):
        url='http://www.lrts.me/ajax/playlist/2/32551/%d' %i
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        s=requests.get(url=url,headers=headers)
        #js= s.json()
        #data=js['data']
        print s.text

spider()



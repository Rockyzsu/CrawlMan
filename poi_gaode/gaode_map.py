# -*-coding=utf-8-*-

# @Time : 2018/12/6 10:39
# @File : gaode_map.py
import requests
from math import radians, cos, sin, asin, sqrt
import config
import json

def demo():
    key=config.key
    url =f'https://restapi.amap.com/v3/place/polygon?polygon=116.460988,40.006919|116.48231,40.007381|116.47516,39.99713|116.472596,39.985227|116.45669,39.984989|116.460988,40.006919&keywords=kfc&output=json&key={key}'
    r = requests.get(url)
    print(r.json())

def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里

    return c * r * 1000


def long_lati_change():
    lbs = [(22.7100061372,113.7915802002),
     (22.7866273171,114.3717956543),
     (22.5404642212,113.9189529419),
     (22.5487084710,114.2375564575),
     (22.6586902908,114.2598724365),
           ]
    for i in lbs:
        print(f'{i[1]},{i[0]}|',end='')
# demo()
# 114.04308499999999,22.527853|114.04808499999999,22.522853
lati1,long1=22.527853,114.04308499999999
lati2,long2=22.522853,114.04808499999999
print(haversine(long1,lati1,long2,lati2))
# long_lati_change()


            

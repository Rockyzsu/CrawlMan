# -*-coding=utf-8-*-

# @Time : 2018/12/13 13:47
# @File : utility.py

import os

# 获取headers

def get_header(header_file='headers.txt'):
    path = os.path.dirname(__file__)
    header_path = os.path.join(path,'headers',header_file)
    if not os.path.exists(header_path):
        return None

    with open(header_path) as fp:
        data = fp.readlines()
    dictionary = dict()

    for line in data:
        line = line.strip()
        line = line.replace(' ', '')
        dictionary[line.split(":")[0].strip()] = ':'.join(
            line.split(":")[1:])

    if 'Content-Length' in dictionary:
        del dictionary['Content-Length']

    return dictionary
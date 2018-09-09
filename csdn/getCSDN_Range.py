# -*-coding=utf-8-*-
# Get your range of csdn
__author__ = 'rocky'
import requests
import re
import time

link = 'http://blog.csdn.net/yagamil/article/details/52858314'
user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
header = {"User-Agent": user_agent}
req = requests.get(link, headers=header)
content =req.text
p = re.search(r' <dl title="(\d+)">',content).group(1)
today = time.strftime("%Y-%m-%d")
f = open(r"D:\OneDrive\Stock_Data\csdn_range.txt", 'a')
contents = today + '\t' + p + '\n'
f.write(contents)
f.close()
